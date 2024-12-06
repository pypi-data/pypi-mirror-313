from abc import ABC
from typing import TypedDict, Iterator

from ximalaya.client import XimalayaClient


class FollowingInfo(TypedDict):
    uid: int
    coverPath: str
    anchorNickName: str
    background: str
    description: str
    url: str
    grade: int
    mvpGrade: int
    gradeType: int
    trackCount: int
    albumCount: int
    followerCount: int
    followingCount: int
    isFollow: bool
    beFollow: bool
    isBlack: bool
    logoType: int
    ptitle: str


class FollowingPageInfo(TypedDict):
    totalCount: int
    followInfoList: list[FollowingInfo]


class FollowingResponse(TypedDict):
    ret: int
    msg: str
    data: dict[{'followingsPageInfo': list[FollowingInfo]}]
    page: int
    pageSize: int
    totalCount: int
    uid: int
    maxCount: int


class SubscriptInfo(TypedDict):
    albumSubscriptValue: int
    url: str


class AlbumInfo(TypedDict):
    albumId: int
    albumPlayCount: int
    albumTrackCount: int
    albumCoverPath: str
    albumTitle: str
    albumUserNickName: str
    anchorId: int
    anchorGrade: int
    mvpGrade: int
    isDeleted: bool
    isPaid: bool
    isFinished: int
    anchorUrl: str
    albumUrl: str
    intro: str
    vipType: int
    logoType: int
    subscriptInfo: SubscriptInfo
    albumSubscript: int


class AlbumsResponse(TypedDict):
    currentUid: int
    total: int
    pageNum: int
    pageSize: int
    albums: list[AlbumInfo]


class PubInfo(TypedDict):
    id: int
    title: str
    subTitle: str
    coverPath: str
    isFinished: bool
    isPaid: bool
    anchorUrl: str
    anchorNickname: str
    anchorUid: int
    playCount: int
    trackCount: int
    albumUrl: str
    description: str
    vipType: int
    albumSubscript: int


class PubPageInfo(TypedDict):
    totalCount: int
    pubInfoList: list[PubInfo]


class TrackInfo(TypedDict):
    trackId: int
    title: str
    trackUrl: str
    coverPath: str
    createTimeAsString: str
    albumId: int
    albumTitle: str
    albumUrl: str
    anchorUid: int
    anchorUrl: str
    nickname: str
    durationAsString: str
    playCount: int
    showLikeBtn: bool
    isLike: bool
    isPaid: bool
    isRelay: bool
    showDownloadBtn: bool
    showCommentBtn: bool
    showForwardBtn: bool
    isVideo: bool
    videoCover: str
    breakSecond: int
    length: int
    isAlbumShow: bool


class TrackPageInfo(TypedDict):
    totalCount: int
    trackInfoList: list[TrackInfo]


class SubscriptionPageInfo(TypedDict):
    privateSub: bool
    totalCount: int
    subscribeInfoList: list


class FansInfo(TypedDict):
    uid: int
    coverPath: str
    anchorNickName: str
    background: str
    url: str
    grade: int
    mvpGrade: int
    gradeType: int
    trackCount: int
    albumCount: int
    followerCount: int
    followingCount: int
    isFollow: bool
    beFollow: bool
    isBlack: bool
    logoType: int


class FansPageInfo(TypedDict):
    totalCount: int
    fansInfoList: list[FansInfo]


class UserDetailedInfo(TypedDict):
    uid: int
    pubPageInfo: PubPageInfo
    trackPageInfo: TrackPageInfo
    subscriptionPageInfo: SubscriptionPageInfo
    followingPageInfo: FollowingPageInfo


class UserBasicInfo(TypedDict):
    uid: int
    nickName: str
    cover: str
    background: str
    isVip: bool
    constellationType: int
    personalSignature: str
    personalDescription: str
    fansCount: int
    gender: int
    birthMonth: int
    birthDay: int
    province: str
    city: str
    anchorGrade: int
    mvpGrade: int
    anchorGradeType: int
    isMusician: bool
    anchorUrl: str
    logoType: int
    followingCount: int
    tracksCount: int
    albumsCount: int
    albumCountReal: int
    userCompany: str
    qualificationGuideInfos: list[str]


class UserSubscription(TypedDict):
    id: int
    title: str
    subTitle: str
    description: str
    coverPath: str
    isFinished: bool
    isPaid: bool
    anchor: dict[{'anchorUrl': str, 'anchorNickName': str, 'anchorUid': int, 'anchorCoverPath': str, 'logoType': int}]
    playCount: int
    trackCount: int
    albumUrl: str
    albumStatus: int
    lastUptrackAt: int
    lastUptrackAtStr: str
    serialState: int
    isTop: bool
    categoryCode: str
    categoryTitle: str
    lastUptrackUrl: str
    lastUptrackTitle: str
    vipType: int
    albumSubscript: int
    albumScore: str


class UserSubscriptionResponse(TypedDict):
    ret: int
    msg: str
    data: dict[{'albumsInfo': list[UserSubscription]}]
    privateSub: bool
    page: int
    pageSize: int
    totalCount: int
    uid: int
    maxCount: int


class ResponsePaginator(ABC, Iterator):
    client: XimalayaClient
    path: str
    page_num: int

    def __init__(self, client: XimalayaClient, path: str, page_num: int = 1):
        self.client = client
        self.path = path
        self.page_num = page_num
