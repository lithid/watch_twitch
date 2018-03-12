#! /usr/local/bin/python

from subprocess import call
from provider.launch_video_provider import LaunchVideoCmdProvider

class LaunchVideoCmdProviderImpl(LaunchVideoCmdProvider):
    def launchVideo(channel_name):
        call(["streamlink", "-p", "mpv --title %s" % channel_name, "twitch.tv/%s" % channel_name])
        return
