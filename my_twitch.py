#! /usr/local/bin/python3

from provider.twitch_client_provider_impl import TwitchClientProviderImpl
from provider.launch_video_provider_impl import LaunchVideoCmdProviderImpl
from model.user_followed_streams import UserFollowedStreams
from model.live_channel import LiveChannel

class TwitchWatcher:

    def __init__(self, client_provider, launch_video_provider):
        self.client_provider = client_provider
        self.launch_video_provider = launch_video_provider

    def select_option(self, live_channels):
        count = 0
        for channel in live_channels:
            print("(%i) %s is currently streaming %s with %s viewers" % (count, channel.name, channel.game, channel.viewers))
            count = count + 1
        print("(x) Exit")

        print("What stream would you like to watch?")
        option = input("> ")
        if option == "x":
            print("Goodbye")
            exit(0)
        elif not option.isdigit():
            print("Invalid selection")
            exit(1)

        return option

    def main(self):
        username = self.client_provider.get_user_display_name()
        print("Finding streams for user: %s\n" % username)

        user_followed_streams = self.client_provider.get_user_followed_streams()
        live_channels = user_followed_streams.live_channels

        option = int(self.select_option(live_channels))
        if 0 <= option <= len(live_channels):
            name = live_channels[option].name
            print("You chose to watch %s    " % name)
            launch_video_provider.launchVideo(name)
        else:
            print("Invalid selection")

if __name__ == "__main__":
    try:
        twitch_client_provider = TwitchClientProviderImpl()
        launch_video_provider = LaunchVideoCmdProviderImpl()
        tw = TwitchWatcher(twitch_client_provider, launch_video_provider)
        tw.main()
    except KeyboardInterrupt:
        print("\nGoodbye")
