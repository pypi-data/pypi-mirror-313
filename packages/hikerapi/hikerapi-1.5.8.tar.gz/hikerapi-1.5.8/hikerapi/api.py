from typing import Any, Dict, List, Optional

from .base import BaseSyncClient
from .helpers import HelperMixin


class Client(BaseSyncClient, HelperMixin):
    def user_a2(self, username: str) -> Dict:
        """User. Get user object"""
        params = {"username": username}
        json = None
        return self._request("get", "/a2/user".format(**{}), params=params, json=json)

    def comments_chunk_gql(
        self,
        media_id: str,
        sort_order: Optional[Any] = None,
        end_cursor: Optional[Any] = None,
    ) -> Dict:
        """Media Comments Chunk. Get comments on a media"""
        params = {
            "media_id": media_id,
            "sort_order": sort_order,
            "end_cursor": end_cursor,
        }
        json = None
        return self._request(
            "get", "/gql/comments/chunk".format(**{}), params=params, json=json
        )

    def comments_threaded_chunk_gql(
        self, media_id: str, comment_id: str, end_cursor: Optional[Any] = None
    ) -> Dict:
        """Media Comments Threaded Chunk. Get threaded comments for comment"""
        params = {
            "media_id": media_id,
            "comment_id": comment_id,
            "end_cursor": end_cursor,
        }
        json = None
        return self._request(
            "get", "/gql/comments/threaded/chunk".format(**{}), params=params, json=json
        )

    def comment_likers_chunk_gql(
        self,
        comment_id: Optional[Any] = None,
        media_id: Optional[Any] = None,
        end_cursor: Optional[str] = None,
    ) -> Dict:
        """Comment Likers Chunk. Get likers on a comment"""
        params = {
            "comment_id": comment_id,
            "media_id": media_id,
            "end_cursor": end_cursor,
        }
        json = None
        return self._request(
            "get", "/gql/comment/likers/chunk".format(**{}), params=params, json=json
        )

    def media_likers_gql(self, media_id: str) -> Dict:
        """Media Likers. Get likers on a media (paging is unavailable on this endpoing)"""
        params = {"media_id": media_id}
        json = None
        return self._request(
            "get", "/gql/media/likers".format(**{}), params=params, json=json
        )

    def user_related_profiles_gql(self, id: str) -> Dict:
        """Related Profiles. Get related profiles by user id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/gql/user/related/profiles".format(**{}), params=params, json=json
        )

    def user_followers_chunk_gql(
        self, user_id: str, end_cursor: Optional[Any] = None
    ) -> Dict:
        """Get a user followers (one request required). Get part (one page) of followers users with cursor"""
        params = {"user_id": user_id, "end_cursor": end_cursor}
        json = None
        return self._request(
            "get", "/gql/user/followers/chunk".format(**{}), params=params, json=json
        )

    def user_following_chunk_gql(
        self, user_id: str, end_cursor: Optional[Any] = None
    ) -> Dict:
        """Get a user following (one request required). Get part (one page) of following users with cursor"""
        params = {"user_id": user_id, "end_cursor": end_cursor}
        json = None
        return self._request(
            "get", "/gql/user/following/chunk".format(**{}), params=params, json=json
        )

    def user_by_id_v1(self, id: str) -> Dict:
        """User By Id. Get user object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/user/by/id".format(**{}), params=params, json=json
        )

    def user_by_username_v1(self, username: str) -> Dict:
        """Get user object by username (one request required). If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user object by username"""
        params = {"username": username}
        json = None
        return self._request(
            "get", "/v1/user/by/username".format(**{}), params=params, json=json
        )

    def user_by_url_v1(self, url: str) -> Dict:
        """Get user object by URL (one request required). Get user object by URL"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/user/by/url".format(**{}), params=params, json=json
        )

    def user_about_v1(self, id: str) -> Dict:
        """User About. Get user object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/user/about".format(**{}), params=params, json=json
        )

    def user_medias_chunk_v1(
        self, user_id: str, end_cursor: Optional[Any] = None
    ) -> Dict:
        """User Medias Chunk. Get part of user medias with cursor"""
        params = {"user_id": user_id, "end_cursor": end_cursor}
        json = None
        return self._request(
            "get", "/v1/user/medias/chunk".format(**{}), params=params, json=json
        )

    def user_medias_pinned_v1(self, user_id: str, amount: Optional[int] = None) -> Dict:
        """Get pinned medias. Get user medias"""
        params = {"user_id": user_id, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/user/medias/pinned".format(**{}), params=params, json=json
        )

    def user_clips_v1(self, user_id: str, amount: Optional[int] = None) -> Dict:
        """Get user clips (one request is required for every 50 media). Get user clips"""
        params = {"user_id": user_id, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/user/clips".format(**{}), params=params, json=json
        )

    def user_clips_chunk_v1(
        self, user_id: str, end_cursor: Optional[Any] = None
    ) -> Dict:
        """User Clips Chunk. Get part of user clips with cursor (default 50 media per request)"""
        params = {"user_id": user_id, "end_cursor": end_cursor}
        json = None
        return self._request(
            "get", "/v1/user/clips/chunk".format(**{}), params=params, json=json
        )

    def user_tag_medias_chunk_v1(
        self, user_id: str, max_id: Optional[str] = None
    ) -> Dict:
        """Usertag Medias Chunk. Get usertag medias"""
        params = {"user_id": user_id, "max_id": max_id}
        json = None
        return self._request(
            "get", "/v1/user/tag/medias/chunk".format(**{}), params=params, json=json
        )

    def user_stories_v1(self, user_id: str, amount: Optional[int] = None) -> Dict:
        """User Stories. Get user stories"""
        params = {"user_id": user_id, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/user/stories".format(**{}), params=params, json=json
        )

    def user_stories_by_username_v1(
        self, username: str, amount: Optional[int] = None
    ) -> Dict:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user stories"""
        params = {"username": username, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/user/stories/by/username".format(**{}), params=params, json=json
        )

    def user_highlights_v1(self, user_id: str, amount: Optional[int] = None) -> Dict:
        """User Highlights. Get user highlights"""
        params = {"user_id": user_id, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/user/highlights".format(**{}), params=params, json=json
        )

    def user_highlights_by_username_v1(
        self, username: str, amount: Optional[int] = None
    ) -> Dict:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user highlights by username"""
        params = {"username": username, "amount": amount}
        json = None
        return self._request(
            "get",
            "/v1/user/highlights/by/username".format(**{}),
            params=params,
            json=json,
        )

    def user_search_followers_v1(self, user_id: str, query: str) -> Dict:
        """Search Followers. Search users by followers"""
        params = {"user_id": user_id, "query": query}
        json = None
        return self._request(
            "get", "/v1/user/search/followers".format(**{}), params=params, json=json
        )

    def user_search_following_v1(self, user_id: str, query: str) -> Dict:
        """Search Following. Search users by following users"""
        params = {"user_id": user_id, "query": query}
        json = None
        return self._request(
            "get", "/v1/user/search/following".format(**{}), params=params, json=json
        )

    def user_following_chunk_v1(
        self, user_id: str, max_id: Optional[str] = None
    ) -> Dict:
        """Get a user following (one request required). Get part (one page) of following users with cursor"""
        params = {"user_id": user_id, "max_id": max_id}
        json = None
        return self._request(
            "get", "/v1/user/following/chunk".format(**{}), params=params, json=json
        )

    def user_followers_chunk_v1(
        self, user_id: str, max_id: Optional[str] = None
    ) -> Dict:
        """Get a user followers (one request required). Get part (one page) of followers users with cursor"""
        params = {"user_id": user_id, "max_id": max_id}
        json = None
        return self._request(
            "get", "/v1/user/followers/chunk".format(**{}), params=params, json=json
        )

    def user_web_profile_info_v1(self, username: str) -> Dict:
        """Web Profile Info"""
        params = {"username": username}
        json = None
        return self._request(
            "get", "/v1/user/web_profile_info".format(**{}), params=params, json=json
        )

    def media_by_id_v1(self, id: str) -> Dict:
        """Media By Id. Get media object"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/media/by/id".format(**{}), params=params, json=json
        )

    def media_by_code_v1(self, code: str) -> Dict:
        """Media By Code. Get media object"""
        params = {"code": code}
        json = None
        return self._request(
            "get", "/v1/media/by/code".format(**{}), params=params, json=json
        )

    def media_by_url_v1(self, url: str) -> Dict:
        """Attention! Use with (https://ins...ram.com/p/CA2aJYrg6cZ/). Get media object"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/media/by/url".format(**{}), params=params, json=json
        )

    def media_insight_v1(self, media_id: str) -> Dict:
        """Insights Media. Get media insight"""
        params = {"media_id": media_id}
        json = None
        return self._request(
            "get", "/v1/media/insight".format(**{}), params=params, json=json
        )

    def media_comments_chunk_v1(
        self,
        id: str,
        min_id: Optional[str] = None,
        max_id: Optional[str] = None,
        can_support_threading: Optional[Any] = None,
    ) -> Dict:
        """Get media comments (one request return 15 comments). Get comments on a media"""
        params = {
            "id": id,
            "min_id": min_id,
            "max_id": max_id,
            "can_support_threading": can_support_threading,
        }
        json = None
        return self._request(
            "get", "/v1/media/comments/chunk".format(**{}), params=params, json=json
        )

    def media_likers_v1(self, id: str) -> Dict:
        """Media Likers. Get user's likers"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/media/likers".format(**{}), params=params, json=json
        )

    def media_user_v1(self, media_id: str) -> Dict:
        """Media User. Get author of the media"""
        params = {"media_id": media_id}
        json = None
        return self._request(
            "get", "/v1/media/user".format(**{}), params=params, json=json
        )

    def media_oembed_v1(self, url: str) -> Dict:
        """Media Oembed. Return info about media and user from post URL"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/media/oembed".format(**{}), params=params, json=json
        )

    def media_code_from_pk_v1(self, pk: str) -> Dict:
        """Media Code From Pk. Get media code from pk"""
        params = {"pk": pk}
        json = None
        return self._request(
            "get", "/v1/media/code/from/pk".format(**{}), params=params, json=json
        )

    def media_pk_from_code_v1(self, code: str) -> Dict:
        """Media Pk From Code. Get media pk from code"""
        params = {"code": code}
        json = None
        return self._request(
            "get", "/v1/media/pk/from/code".format(**{}), params=params, json=json
        )

    def media_pk_from_url_v1(self, url: str) -> Dict:
        """Attention! Use with (https://ins...ram.com/p/CA2aJYrg6cZ/). Get Media pk from URL"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/media/pk/from/url".format(**{}), params=params, json=json
        )

    def story_by_id_v1(self, id: str) -> Dict:
        """Story By Id. Get story object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/story/by/id".format(**{}), params=params, json=json
        )

    def story_by_url_v1(self, url: str) -> Dict:
        """Attention! To work with /s/ links, call /v1/share/by/url first. Get story object by id"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/story/by/url".format(**{}), params=params, json=json
        )

    def story_download_v1(self, id: str) -> Dict:
        """Story Download. Download story media by story id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/story/download".format(**{}), params=params, json=json
        )

    def story_download_by_url_v1(self, url: str) -> Dict:
        """Download story file by URL to file. Download story file by URL to file
        (you can take it from "/v1/story/by/id" or "/v1/story/by/url")
        Example: https://scontent-lga3-1.cdnins...ram.com/v/t66.30100-16/
            310890533_1622838408176007_5601749632271872566_n.mp4?efg=..."""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/story/download/by/url".format(**{}), params=params, json=json
        )

    def story_download_by_story_url_v1(self, url: str) -> Dict:
        """Download story file by story URL. Download story file by story URL
        Example: https://ins...ram.com/stories/example/30038568123745341231284"""
        params = {"url": url}
        json = None
        return self._request(
            "get",
            "/v1/story/download/by/story/url".format(**{}),
            params=params,
            json=json,
        )

    def location_by_id_v1(self, id: str) -> Dict:
        """Location By Id. Get location object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v1/location/by/id".format(**{}), params=params, json=json
        )

    def location_medias_top_v1(
        self, location_pk: int, amount: Optional[int] = None
    ) -> Dict:
        """Location Medias Top V1. Get location top medias"""
        params = {"location_pk": location_pk, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/location/medias/top".format(**{}), params=params, json=json
        )

    def location_medias_recent_v1(
        self, location_pk: int, amount: Optional[int] = None
    ) -> Dict:
        """Location Medias Recent V1. Get location recent medias"""
        params = {"location_pk": location_pk, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/location/medias/recent".format(**{}), params=params, json=json
        )

    def location_medias_top_chunk_v1(
        self, location_pk: int, max_id: Optional[str] = None
    ) -> Dict:
        """Location Medias Top Chunk. Get location chunk of top medias"""
        params = {"location_pk": location_pk, "max_id": max_id}
        json = None
        return self._request(
            "get",
            "/v1/location/medias/top/chunk".format(**{}),
            params=params,
            json=json,
        )

    def location_medias_recent_chunk_v1(
        self, location_pk: int, max_id: Optional[str] = None
    ) -> Dict:
        """Location Medias Recent Chunk. Get location chunk of recent medias"""
        params = {"location_pk": location_pk, "max_id": max_id}
        json = None
        return self._request(
            "get",
            "/v1/location/medias/recent/chunk".format(**{}),
            params=params,
            json=json,
        )

    def location_search_v1(self, lat: float, lng: float) -> Dict:
        """Location Search. Get locations using lat and long"""
        params = {"lat": lat, "lng": lng}
        json = None
        return self._request(
            "get", "/v1/location/search".format(**{}), params=params, json=json
        )

    def location_guides_v1(self, location_pk: int) -> Dict:
        """Location Guides V1. Get location guides"""
        params = {"location_pk": location_pk}
        json = None
        return self._request(
            "get", "/v1/location/guides".format(**{}), params=params, json=json
        )

    def search_hashtags_v1(self, query: str) -> Dict:
        """Search Hashtags. Search hashtags"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v1/search/hashtags".format(**{}), params=params, json=json
        )

    def search_users_v1(self, query: str) -> Dict:
        """Search Users. Search users"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v1/search/users".format(**{}), params=params, json=json
        )

    def search_music_v1(self, query: str) -> Dict:
        """Search Music. Search music"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v1/search/music".format(**{}), params=params, json=json
        )

    def fbsearch_places_v1(
        self, query: str, lat: Optional[Any] = None, lng: Optional[Any] = None
    ) -> Dict:
        """Fbsearch Places. Search locations"""
        params = {"query": query, "lat": lat, "lng": lng}
        json = None
        return self._request(
            "get", "/v1/fbsearch/places".format(**{}), params=params, json=json
        )

    def fbsearch_topsearch_v1(self, query: str) -> Dict:
        """Fbsearch Topsearch. Topsearch"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v1/fbsearch/topsearch".format(**{}), params=params, json=json
        )

    def fbsearch_topsearch_hashtags_v1(self, query: str) -> Dict:
        """Web Search Topsearch Hashtags. Search hashtags via topsearch"""
        params = {"query": query}
        json = None
        return self._request(
            "get",
            "/v1/fbsearch/topsearch/hashtags".format(**{}),
            params=params,
            json=json,
        )

    def hashtag_by_name_v1(self, name: str) -> Dict:
        """Hashtag By Name. Get hashtag object by name"""
        params = {"name": name}
        json = None
        return self._request(
            "get", "/v1/hashtag/by/name".format(**{}), params=params, json=json
        )

    def hashtag_medias_top_v1(self, name: str, amount: Optional[int] = None) -> Dict:
        """Hashtag Medias Top. Get hashtag medias top"""
        params = {"name": name, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/hashtag/medias/top".format(**{}), params=params, json=json
        )

    def hashtag_medias_top_chunk_v1(
        self, name: str, max_id: Optional[str] = None
    ) -> Dict:
        """Hashtag Medias Top Chunk. Get hashtag chunk of top medias"""
        params = {"name": name, "max_id": max_id}
        json = None
        return self._request(
            "get", "/v1/hashtag/medias/top/chunk".format(**{}), params=params, json=json
        )

    def hashtag_medias_top_recent_chunk_v1(
        self, name: str, max_id: Optional[str] = None
    ) -> Dict:
        """Hashtag Medias Top Recent Chunk. Get hashtag chunk of recent medias"""
        params = {"name": name, "max_id": max_id}
        json = None
        return self._request(
            "get",
            "/v1/hashtag/medias/top/recent/chunk".format(**{}),
            params=params,
            json=json,
        )

    def hashtag_medias_clips_v1(self, name: str, amount: Optional[int] = None) -> Dict:
        """Hashtag Medias Clips. Get hashtag clips (reels)"""
        params = {"name": name, "amount": amount}
        json = None
        return self._request(
            "get", "/v1/hashtag/medias/clips".format(**{}), params=params, json=json
        )

    def hashtag_medias_clips_chunk_v1(
        self, name: str, max_id: Optional[str] = None
    ) -> Dict:
        """Hashtag Medias Clips Chunk. Get hashtag chunk of clips (reels)"""
        params = {"name": name, "max_id": max_id}
        json = None
        return self._request(
            "get",
            "/v1/hashtag/medias/clips/chunk".format(**{}),
            params=params,
            json=json,
        )

    def highlight_by_url_v1(self, url: str) -> Dict:
        """Attention! To work with /s/ links, call /v1/share/by/url first. Get highlight object by id"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/highlight/by/url".format(**{}), params=params, json=json
        )

    def share_by_code_v1(self, code: str) -> Dict:
        """Works for stories and highlights only or use (/v1/media/by/url, /v1/story/by/url). Get share object by code (aGlnaGxpZ2h0OjE4MTQ2MjE2Njk4MDIyMTc0 ->
        {"pk": 18146216698022176, "type": "highlight"})"""
        params = {"code": code}
        json = None
        return self._request(
            "get", "/v1/share/by/code".format(**{}), params=params, json=json
        )

    def share_by_url_v1(self, url: str) -> Dict:
        """Works for stories and highlights only ig...m.com/s/aGln(link must contain /s/) or use (/v1/media/by/url, /v1/story/by/url). Get share object by url (
        https://www.ins...ram.com/s/aGlnaGxpZ2h0OjE4MTQ2MjE2Njk4MDIyMTc0 ->
        {"pk": 18146216698022176, "type": "highlight"})"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/share/by/url".format(**{}), params=params, json=json
        )

    def share_reel_by_url_v1(self, url: str) -> Dict:
        """Works for reel (clips) only"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v1/share/reel/by/url".format(**{}), params=params, json=json
        )

    def user_by_id_v2(self, id: str) -> Dict:
        """User By Id. Get user object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/user/by/id".format(**{}), params=params, json=json
        )

    def user_by_username_v2(self, username: str) -> Dict:
        """Get user object by username (one request required). If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user object by username"""
        params = {"username": username}
        json = None
        return self._request(
            "get", "/v2/user/by/username".format(**{}), params=params, json=json
        )

    def userstream_by_username_v2(self, username: str) -> Dict:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get userstream (info) by username"""
        params = {"username": username}
        json = None
        return self._request(
            "get", "/v2/userstream/by/username".format(**{}), params=params, json=json
        )

    def user_stories_v2(self, user_id: str) -> Dict:
        """User Stories. Get user stories"""
        params = {"user_id": user_id}
        json = None
        return self._request(
            "get", "/v2/user/stories".format(**{}), params=params, json=json
        )

    def user_stories_by_username_v2(self, username: str) -> Dict:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user stories"""
        params = {"username": username}
        json = None
        return self._request(
            "get", "/v2/user/stories/by/username".format(**{}), params=params, json=json
        )

    def user_medias_v2(
        self, user_id: Optional[str] = None, page_id: Optional[str] = None
    ) -> Dict:
        """User Medias. Get user medias. Results chunk."""
        params = {"user_id": user_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/user/medias".format(**{}), params=params, json=json
        )

    def user_medias(
        self,
        user_id: Optional[str] = None,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """User Medias. Get user medias. Results chunk."""
        params = {"user_id": user_id, "page_id": page_id}
        return self._paging_request(
            "/v2/user/medias",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_clips_v2(
        self, user_id: Optional[str] = None, page_id: Optional[str] = None
    ) -> Dict:
        """User Clips. Get user clips."""
        params = {"user_id": user_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/user/clips".format(**{}), params=params, json=json
        )

    def user_clips(
        self,
        user_id: Optional[str] = None,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """User Clips. Get user clips."""
        params = {"user_id": user_id, "page_id": page_id}
        return self._paging_request(
            "/v2/user/clips",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_following_v2(
        self, user_id: Optional[str] = None, page_id: Optional[str] = None
    ) -> Dict:
        """Get a user following (one request required). Get part (one page) of following users"""
        params = {"user_id": user_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/user/following".format(**{}), params=params, json=json
        )

    def user_following(
        self,
        user_id: Optional[str] = None,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Get a user following (one request required). Get part (one page) of following users"""
        params = {"user_id": user_id, "page_id": page_id}
        return self._paging_request(
            "/v2/user/following",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_followers_v2(
        self, user_id: Optional[str] = None, page_id: Optional[str] = None
    ) -> Dict:
        """Get a user followers (one request required). Get part (one page) of followers users with cursor"""
        params = {"user_id": user_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/user/followers".format(**{}), params=params, json=json
        )

    def user_followers(
        self,
        user_id: Optional[str] = None,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Get a user followers (one request required). Get part (one page) of followers users with cursor"""
        params = {"user_id": user_id, "page_id": page_id}
        return self._paging_request(
            "/v2/user/followers",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_tag_medias_v2(
        self, user_id: Optional[str] = None, page_id: Optional[str] = None
    ) -> Dict:
        """Get medias where user is tagged. Get usertag medias"""
        params = {"user_id": user_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/user/tag/medias".format(**{}), params=params, json=json
        )

    def user_tag_medias(
        self,
        user_id: Optional[str] = None,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Get medias where user is tagged. Get usertag medias"""
        params = {"user_id": user_id, "page_id": page_id}
        return self._paging_request(
            "/v2/user/tag/medias",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_highlights_v2(self, user_id: str, amount: Optional[int] = None) -> Dict:
        """User Highlights. Get user highlights"""
        params = {"user_id": user_id, "amount": amount}
        json = None
        return self._request(
            "get", "/v2/user/highlights".format(**{}), params=params, json=json
        )

    def user_highlights(
        self,
        user_id: str,
        amount: Optional[int] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """User Highlights. Get user highlights"""
        params = {"user_id": user_id, "amount": amount}
        return self._paging_request(
            "/v2/user/highlights",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def user_highlights_by_username_v2(
        self, username: str, amount: Optional[int] = None
    ) -> Dict:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user highlights by username"""
        params = {"username": username, "amount": amount}
        json = None
        return self._request(
            "get",
            "/v2/user/highlights/by/username".format(**{}),
            params=params,
            json=json,
        )

    def user_highlights_by_username(
        self,
        username: str,
        amount: Optional[int] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """If speed is crucial, it's more efficient to use the by/id endpoint for quicker responses.. Get user highlights by username"""
        params = {"username": username, "amount": amount}
        return self._paging_request(
            "/v2/user/highlights/by/username",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def media_info_by_id_v2(self, id: str) -> Dict:
        """Media Info By Id. Get media object"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/media/info/by/id".format(**{}), params=params, json=json
        )

    def media_info_by_code_v2(self, code: str) -> Dict:
        """Media Info By Code. Get media object"""
        params = {"code": code}
        json = None
        return self._request(
            "get", "/v2/media/info/by/code".format(**{}), params=params, json=json
        )

    def media_info_by_url_v2(self, url: str) -> Dict:
        """Attention! Use with (https://ins...ram.com/p/CA2aJYrg6cZ/). Get media object"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v2/media/info/by/url".format(**{}), params=params, json=json
        )

    def media_comments_v2(
        self,
        id: str,
        can_support_threading: Optional[Any] = None,
        page_id: Optional[Any] = None,
    ) -> Dict:
        """Get media comments (one request return 15 comments). Get comments on a media"""
        params = {
            "id": id,
            "can_support_threading": can_support_threading,
            "page_id": page_id,
        }
        json = None
        return self._request(
            "get", "/v2/media/comments".format(**{}), params=params, json=json
        )

    def media_comments(
        self,
        id: str,
        can_support_threading: Optional[Any] = None,
        page_id: Optional[Any] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Get media comments (one request return 15 comments). Get comments on a media"""
        params = {
            "id": id,
            "can_support_threading": can_support_threading,
            "page_id": page_id,
        }
        return self._paging_request(
            "/v2/media/comments",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def media_likers_v2(self, id: str) -> Dict:
        """Media Likers. Get user's likers"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/media/likers".format(**{}), params=params, json=json
        )

    def media_template_v2(self, id: str) -> Dict:
        """Media Template. Get media template"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/media/template".format(**{}), params=params, json=json
        )

    def media_comment_offensive_v2(self, media_id: str, comment: str) -> Dict:
        """Media Check Offensive Comment. Whether to receive an offensive comment"""
        params = {"media_id": media_id, "comment": comment}
        json = None
        return self._request(
            "get", "/v2/media/comment/offensive".format(**{}), params=params, json=json
        )

    def media_comment_offensive(
        self,
        media_id: str,
        comment: str,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Media Check Offensive Comment. Whether to receive an offensive comment"""
        params = {"media_id": media_id, "comment": comment}
        return self._paging_request(
            "/v2/media/comment/offensive",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def story_by_id_v2(self, id: str) -> Dict:
        """Story By Id. Get story object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/story/by/id".format(**{}), params=params, json=json
        )

    def story_by_url_v2(self, url: str) -> Dict:
        """Attention! To work with /s/ links, call /v1/share/by/url first. Get story object by id"""
        params = {"url": url}
        json = None
        return self._request(
            "get", "/v2/story/by/url".format(**{}), params=params, json=json
        )

    def track_by_canonical_id_v2(
        self, canonical_id: str, page_id: Optional[str] = None
    ) -> Dict:
        """Track By Canonical Id. Get music track object by canonical_id"""
        params = {"canonical_id": canonical_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/track/by/canonical/id".format(**{}), params=params, json=json
        )

    def track_by_canonical_id(
        self,
        canonical_id: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Track By Canonical Id. Get music track object by canonical_id"""
        params = {"canonical_id": canonical_id, "page_id": page_id}
        return self._paging_request(
            "/v2/track/by/canonical/id",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def track_by_id_v2(self, track_id: str, page_id: Optional[str] = None) -> Dict:
        """Track By Id. Get music track object by id"""
        params = {"track_id": track_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/track/by/id".format(**{}), params=params, json=json
        )

    def track_by_id(
        self,
        track_id: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Track By Id. Get music track object by id"""
        params = {"track_id": track_id, "page_id": page_id}
        return self._paging_request(
            "/v2/track/by/id",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def track_stream_by_id_v2(
        self, track_id: str, page_id: Optional[str] = None
    ) -> Dict:
        """Track Stream By Id. Get music track object by id"""
        params = {"track_id": track_id, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/track/stream/by/id".format(**{}), params=params, json=json
        )

    def track_stream_by_id(
        self,
        track_id: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Track Stream By Id. Get music track object by id"""
        params = {"track_id": track_id, "page_id": page_id}
        return self._paging_request(
            "/v2/track/stream/by/id",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def hashtag_by_name_v2(self, name: str) -> Dict:
        """Hashtag By Name. Get hashtag object by name"""
        params = {"name": name}
        json = None
        return self._request(
            "get", "/v2/hashtag/by/name".format(**{}), params=params, json=json
        )

    def hashtag_medias_top_v2(self, name: str, page_id: Optional[str] = None) -> Dict:
        """Hashtag Medias Top Chunk. Get hashtag chunk of top medias"""
        params = {"name": name, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/hashtag/medias/top".format(**{}), params=params, json=json
        )

    def hashtag_medias_top(
        self,
        name: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Hashtag Medias Top Chunk. Get hashtag chunk of top medias"""
        params = {"name": name, "page_id": page_id}
        return self._paging_request(
            "/v2/hashtag/medias/top",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def hashtag_medias_recent_v2(
        self, name: str, page_id: Optional[str] = None
    ) -> Dict:
        """Hashtag Medias Recent Chunk. Get hashtag chunk of recent medias"""
        params = {"name": name, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/hashtag/medias/recent".format(**{}), params=params, json=json
        )

    def hashtag_medias_recent(
        self,
        name: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Hashtag Medias Recent Chunk. Get hashtag chunk of recent medias"""
        params = {"name": name, "page_id": page_id}
        return self._paging_request(
            "/v2/hashtag/medias/recent",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def hashtag_medias_clips_v2(self, name: str, page_id: Optional[str] = None) -> Dict:
        """Hashtag Medias Clips Chunk. Get hashtag chunk of clips (reels)"""
        params = {"name": name, "page_id": page_id}
        json = None
        return self._request(
            "get", "/v2/hashtag/medias/clips".format(**{}), params=params, json=json
        )

    def hashtag_medias_clips(
        self,
        name: str,
        page_id: Optional[str] = None,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Hashtag Medias Clips Chunk. Get hashtag chunk of clips (reels)"""
        params = {"name": name, "page_id": page_id}
        return self._paging_request(
            "/v2/hashtag/medias/clips",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def highlight_by_id_v2(self, id: str) -> Dict:
        """Highlight By Id. Get highlight object by id"""
        params = {"id": id}
        json = None
        return self._request(
            "get", "/v2/highlight/by/id".format(**{}), params=params, json=json
        )

    def highlight_by_id(
        self,
        id: str,
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        """Highlight By Id. Get highlight object by id"""
        params = {"id": id}
        return self._paging_request(
            "/v2/highlight/by/id",
            params=params,
            count=count,
            container=container,
            max_requests=max_requests,
        )

    def search_hashtags_v2(self, query: str, page_token: Optional[str] = None) -> Dict:
        """Search Hashtags. Search hashtags"""
        params = {"query": query, "page_token": page_token}
        json = None
        return self._request(
            "get", "/v2/search/hashtags".format(**{}), params=params, json=json
        )

    def search_accounts_v2(self, query: str, page_token: Optional[str] = None) -> Dict:
        """Search Accounts. Search accounts"""
        params = {"query": query, "page_token": page_token}
        json = None
        return self._request(
            "get", "/v2/search/accounts".format(**{}), params=params, json=json
        )

    def search_music_v2(self, query: str, next_max_id: Optional[str] = None) -> Dict:
        """Search Music. Search music"""
        params = {"query": query, "next_max_id": next_max_id}
        json = None
        return self._request(
            "get", "/v2/search/music".format(**{}), params=params, json=json
        )

    def search_places_v2(self, query: str) -> Dict:
        """Search Places. Search places"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v2/search/places".format(**{}), params=params, json=json
        )

    def search_topsearch_v2(
        self, query: str, next_max_id: Optional[str] = None
    ) -> Dict:
        """Search Top. Search top content by keyword"""
        params = {"query": query, "next_max_id": next_max_id}
        json = None
        return self._request(
            "get", "/v2/search/topsearch".format(**{}), params=params, json=json
        )

    def search_reels_v2(self, query: str, reels_max_id: Optional[str] = None) -> Dict:
        """Search Reels. Search top content by keyword"""
        params = {"query": query, "reels_max_id": reels_max_id}
        json = None
        return self._request(
            "get", "/v2/search/reels".format(**{}), params=params, json=json
        )

    def fbsearch_accounts_v2(
        self, query: str, page_token: Optional[str] = None
    ) -> Dict:
        """Fbsearch Accounts. Search accounts"""
        params = {"query": query, "page_token": page_token}
        json = None
        return self._request(
            "get", "/v2/fbsearch/accounts".format(**{}), params=params, json=json
        )

    def fbsearch_places_v2(self, query: str) -> Dict:
        """Fbsearch Places. Search places"""
        params = {"query": query}
        json = None
        return self._request(
            "get", "/v2/fbsearch/places".format(**{}), params=params, json=json
        )

    def fbsearch_topsearch_v2(
        self, query: str, next_max_id: Optional[str] = None
    ) -> Dict:
        """Fbsearch Top. Search top content by keyword"""
        params = {"query": query, "next_max_id": next_max_id}
        json = None
        return self._request(
            "get", "/v2/fbsearch/topsearch".format(**{}), params=params, json=json
        )

    def fbsearch_reels_v2(self, query: str, reels_max_id: Optional[str] = None) -> Dict:
        """Fbsearch Reels. Search top content by keyword"""
        params = {"query": query, "reels_max_id": reels_max_id}
        json = None
        return self._request(
            "get", "/v2/fbsearch/reels".format(**{}), params=params, json=json
        )
