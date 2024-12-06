from ximalaya.api.typing import ResponsePaginator, AlbumInfo
from ximalaya.client import XimalayaClient


class AlbumsResponsePagination(ResponsePaginator):
    def __next__(self) -> list[AlbumInfo]:
        data = self.client.get(f'{self.path}&pageNum={self.page_num}')['data']

        albums = data['albums']

        if len(albums) == 0 or data['total'] == 0:
            raise StopIteration()

        self.page_num += 1

        return albums


def get_category_albums(client: XimalayaClient, category_id: int, page_size: int = 56, sort_by: int = 1) -> AlbumsResponsePagination:
    return AlbumsResponsePagination(client=client, path=f'/revision/category/v2/albums?pageSize={page_size}&sort={sort_by}&categoryId={category_id}')
