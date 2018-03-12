#! /usr/local/bin/python

from twitch import TwitchClient
from .twitch_client_provider import TwitchClientProvider
from model.live_channel import LiveChannel
from model.user_followed_streams import UserFollowedStreams

class TwitchClientProviderImpl(TwitchClientProvider):

    def __init__(self):
        self.client = TwitchClient()

    def get_user_display_name(self):
        return self.__get_twitch_username(self.__get_twitch_user());

    def get_user_followed_streams(self):
        user = self.__get_twitch_user()
        follows = self.__get_twitch_followed_channels(user.get("id"))
        channel_ids = self.__get_twitch_followed_channel_ids(follows)
        live_channels = self.__get_twitch_live_channels(channel_ids)
        return UserFollowedStreams(self.__get_twitch_username(user), live_channels)

    def __get_twitch_username(self, user):
        return user.get("display_name")

    def __get_twitch_user(self):
        return self.client.users.get()

    def __get_twitch_followed_channels(self, twitch_id):
        return self.client.users.get_follows(twitch_id, 100, 0, "desc", "last_broadcast")

    def __get_twitch_streams(self, channel_ids):
        return self.client.streams.get_live_streams(channel_ids)

    def __get_twitch_followed_channel_ids(self, follow_list):
        channel_ids = ""
        for follow in follow_list:
            this_channel = follow.get("channel")
            if (len(channel_ids) == 0):
                channel_ids = "%s" % this_channel.get("id")
            else:
                channel_ids = "%s,%s" % (channel_ids, this_channel.get("id"))

        return channel_ids

    def __get_twitch_live_channels(self, channel_ids):
        live_channels = []
        streams = self.__get_twitch_streams(channel_ids)
        for stream in streams:
            viewers = stream.get("viewers")
            game = stream.get("game")

            c = stream.get("channel")
            name = c.get("display_name")
            live_channels.append(LiveChannel(name, viewers, game))

        return live_channels