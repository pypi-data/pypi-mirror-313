from ximalaya.api.typing import ResponsePaginator, FollowingInfo, UserBasicInfo, UserDetailedInfo, UserSubscription
from ximalaya.client import XimalayaClient


class FollowingResponsePaginator(ResponsePaginator):
    def __next__(self) -> list[FollowingInfo]:
        data = self.client.get(f'{self.path}&page={self.page_num}')['data']

        followings = data['followingsPageInfo']

        if len(followings) == 0:
            raise StopIteration()

        self.page_num += 1

        return followings


class SubscriptionResponsePaginator(ResponsePaginator):
    def __next__(self) -> list[UserSubscription]:
        data = self.client.get(f'{self.path}&page={self.page_num}')['data']

        subs = data['albumsInfo']

        if len(subs) == 0:
            raise StopIteration()

        self.page_num += 1

        return subs


def get_user_followings(client: XimalayaClient, uid: int, page_size: int = 10) -> FollowingResponsePaginator:
    return FollowingResponsePaginator(client=client, path=f'/revision/user/following?uid={uid}&pageSize={page_size}&keyWord=')


def get_user_basic_info(client: XimalayaClient, uid: int) -> UserBasicInfo:
    return client.get(f'/revision/user/basic?uid={uid}')['data']


def get_user_detailed_info(client: XimalayaClient, uid: int) -> UserDetailedInfo:
    return client.get(f'/revision/user?uid={uid}')['data']


def get_user_subscriptions(client: XimalayaClient, uid: int, page_size: int = 10) -> list[UserSubscription]:
    return client.get(f'/revision/user/sub?pageSize={page_size}&keyWord=&uid={uid}')
