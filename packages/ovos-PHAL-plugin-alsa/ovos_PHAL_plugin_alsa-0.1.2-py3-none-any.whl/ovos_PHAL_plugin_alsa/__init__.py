import alsaaudio

from ovos_plugin_manager.phal import PHALPlugin
from os.path import join, dirname
from ovos_utils.log import LOG
from ovos_bus_client import Message
from json_database import JsonConfigXDG
from ovos_utils.system import find_executable, is_process_running
from ovos_plugin_manager.phal import find_phal_plugins


class AlsaValidator:
    @staticmethod
    def validate(config=None):
        """ this method is called before loading the plugin.
        If it returns False the plugin is not loaded.
        This allows a plugin to run platform checks"""
        # any aliases we need here ?
        execs = ["pulseaudio"]
        is_pulse = any((find_executable(e) or is_process_running(e)
                        for e in execs))

        # check if pulseaudio is installed in system
        # if missing load alsa
        if not is_pulse:
            return True

        # check if pulse plugin is installed
        # if missing load alsa
        plugs = list(find_phal_plugins().keys())
        if "ovos-PHAL-plugin-pulseaudio" not in plugs:
            return True

        # pulseaudio installed + companion plugin, do not load alsa
        return False


class AlsaVolumeControlPlugin(PHALPlugin):
    validator = AlsaValidator

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-alsa", config=config)
        self.settings = JsonConfigXDG(self.name, subfolder="OpenVoiceOS")
        self.alsa = AlsaControl()
        self.bus.on("mycroft.volume.get", self.handle_volume_request)
        self.bus.on("mycroft.volume.set", self.handle_volume_change)
        self.bus.on("mycroft.volume.increase", self.handle_volume_increase)
        self.bus.on("mycroft.volume.decrease", self.handle_volume_decrease)
        self.bus.on("mycroft.volume.mute", self.handle_mute_request)
        self.bus.on("mycroft.volume.unmute", self.handle_unmute_request)
        self.bus.on("mycroft.volume.mute.toggle", self.handle_mute_toggle_request)

        if self.settings.get("first_boot", True):
            self.set_volume(self.config.get("default_volume", 75))
            self.settings["first_boot"] = False
            self.settings.store()

    def get_volume(self):
        return self.alsa.get_volume_percent()

    def set_volume(self, percent=None, play_sound=True):
        volume = int(percent)
        volume = min(100, volume)
        volume = max(0, volume)
        if play_sound:
            self.bus.emit(Message("mycroft.audio.play_sound", {"uri": "snd/blop-mark-diangelo.wav"}))
        self.alsa.set_volume_percent(volume)
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def increase_volume(self, volume_change=None, play_sound=True):
        if not volume_change:
            volume_change = 15
        if play_sound:
            self.bus.emit(Message("mycroft.audio.play_sound", {"uri": "snd/blop-mark-diangelo.wav"}))
        self.alsa.increase_volume(volume_change)
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def decrease_volume(self, volume_change=None, play_sound=True):
        if not volume_change:
            volume_change = -15
        if volume_change > 0:
            volume_change = 0 - volume_change
        if play_sound:
            self.bus.emit(Message("mycroft.audio.play_sound", {"uri": "snd/blop-mark-diangelo.wav"}))
        self.alsa.increase_volume(volume_change)
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def handle_mute_request(self, message):
        self.log.info("User muted audio.")
        self.alsa.mute()
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def handle_unmute_request(self, message):
        self.log.info("User unmuted audio.")
        self.alsa.unmute()
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def handle_mute_toggle_request(self, message):
        self.alsa.toggle_mute()
        muted = self.alsa.is_muted()
        self.log.info(f"User toggled mute. Result: {'muted' if muted else 'unmuted'}")
        # report change
        self.handle_volume_request(Message("mycroft.volume.get"))

    def handle_volume_request(self, message):
        percent = self.get_volume() / 100
        self.bus.emit(message.response({"percent": percent,
                                        "muted": self.alsa.is_muted()}))

    def handle_volume_change(self, message):
        percent = message.data["percent"] * 100
        play_sound = message.data.get("play_sound", True)
        assert isinstance(play_sound, bool)
        self.set_volume(percent, play_sound=play_sound)

    def handle_volume_increase(self, message):
        percent = message.data.get("percent", .10) * 100
        play_sound = message.data.get("play_sound", True)
        assert isinstance(play_sound, bool)
        self.increase_volume(percent, play_sound)

    def handle_volume_decrease(self, message):
        percent = message.data.get("percent", -.10) * 100
        play_sound = message.data.get("play_sound", True)
        assert isinstance(play_sound, bool)
        self.decrease_volume(percent, play_sound)

    def shutdown(self):
        self.bus.remove("mycroft.volume.get", self.handle_volume_request)
        self.bus.remove("mycroft.volume.set", self.handle_volume_change)
        self.bus.remove("mycroft.volume.increase", self.handle_volume_increase)
        self.bus.remove("mycroft.volume.decrease", self.handle_volume_decrease)
        self.bus.remove("mycroft.volume.mute", self.handle_mute_request)
        self.bus.remove("mycroft.volume.unmute", self.handle_unmute_request)
        self.bus.remove("mycroft.volume.mute.toggle", self.handle_mute_toggle_request)
        super().shutdown()


class AlsaControl:
    _mixer = None

    def __init__(self, control=None):
        if control is None:
            control = alsaaudio.mixers()[0]
        self.get_mixer(control)

    @property
    def mixer(self):
        return self._mixer
    
    @property
    def can_mute(self):
        return any(cap in ('Mute', 'Playback Mute', 'Joined Playback Mute')
                   for cap in self.mixer.switchcap())

    def get_mixer(self, control="Master"):
        if self._mixer is None:
            try:
                mixer = alsaaudio.Mixer(control)
            except Exception as e:
                try:
                    mixer = alsaaudio.Mixer(control)
                except Exception as e:
                    try:
                        if control != "Master":
                            LOG.warning("could not allocate requested mixer, "
                                        "falling back to 'Master'")
                            mixer = alsaaudio.Mixer("Master")
                        else:
                            raise
                    except Exception as e:
                        LOG.error("Couldn't allocate mixer")
                        LOG.exception(e)
                        raise
            self._mixer = mixer
        return self.mixer

    def increase_volume(self, percent):
        if self.is_muted():
            self.unmute()
            volume = 0
        else:
            volume = self.get_volume()
            if isinstance(volume, list):
                volume = volume[0]
        volume += percent
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.mixer.setvolume(int(volume))

    def decrease_volume(self, percent):
        if self.is_muted():
            self.unmute()
            volume = 0
        else:
            volume = self.get_volume()
            if isinstance(volume, list):
                volume = volume[0]
        volume -= percent
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.mixer.setvolume(int(volume))

    def set_volume_percent(self, percent):
        self.set_volume(percent)

    def set_volume(self, volume):
        self.unmute()
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.mixer.setvolume(int(volume))

    def volume_range(self):
        return self.mixer.getrange()

    def is_muted(self):
        if not self.can_mute:
            return False
        return bool(self.mixer.getmute()[0])

    def mute(self):
        if not self.can_mute:
            LOG.warning("Trying to mute a non-switchcap mixer")
            return
        return self.mixer.setmute(1)

    def unmute(self):
        if not self.can_mute:
            LOG.warning("Trying to unmute a non-switchcap mixer")
            return
        return self.mixer.setmute(0)

    def toggle_mute(self):
        if not self.can_mute:
            LOG.warning("Trying to toggle mute on a non-switchcap mixer")
            return

        if self.is_muted():
            self.unmute()
        else:
            self.mute()

    def get_volume(self):
        return self.mixer.getvolume()[0]

    def get_volume_percent(self):
        return self.get_volume()
