from typing import List
from collections import defaultdict
from geodesic.bases import _APIObject
from geodesic.client import raise_on_error
from geodesic.config import get_config
from geodesic.descriptors import _StringDescr
from geodesic.service import ServiceClient
from geodesic.utils import deprecated

ted_client = ServiceClient("ted", 1, "share")


class Token(_APIObject):
    """The token class represents the share tokens created when a user shares a dataset through Ted.

    Args:
        **token: values corresponding to the token and the dataset it shares
    """

    token = _StringDescr(
        doc="unique 32-bit token created by Ted and used to access a shared dataset"
    )
    servicer = _StringDescr(doc="the servicer of the dataset shared by the token")
    dataset = _StringDescr(doc="the dataset shared by the token")
    project = _StringDescr(doc="the project of the dataset shared by the token")
    ttl = _StringDescr(doc="the remaining time in seconds until the token expires")

    _limit_setitem = ["token", "servicer", "dataset", "project", "ttl"]

    def __init__(self, **token):
        self.__client = ted_client
        super().__init__(self, **token)

    @property
    def url(self) -> str:
        """Returns the URL that can be used to access a datset shared through Ted.

        Raises:
            requests.HTTPErrror for fault

        Returns:
            the URL to access the token in question
        """
        return "{api_host}/ted/api/v1/share/{token}/".format(
            api_host=get_config().host, token=self.token
        )

    @property
    def feature_service_url(self) -> str:
        """Gets a url to an GeoServices FeatureService.

        Returns a URL pointing to a feature service that can be used in ArcGIS.

        DEPRECATED: use get_feature_service_url instead
        """
        return self.get_feature_service_url()

    @property
    def image_service_url(self) -> str:
        """Gets a url to an GeoServices ImageService.

        Returns a URL pointing to an image service that can be used in ArcGIS.

        DEPRECATED: use get_image_service_url instead
        """
        return self.get_image_service_url()

    @property
    def vector_tile_service_url(self) -> str:
        """Gets a url to an GeoServices VectorTileService.

        Returns a URL pointing to a vector tile service that can be used in ArcGIS.

        DEPRECATED: use get_vector_tile_service_url instead
        """
        return self.get_vector_tile_service_url()

    def get_vector_tile_service_url(self, service_name: str = None):
        """Gets a url to an GeoServices VectorTileService.

        Args:
            service_name: an optional service name to use in place of the dataset name

        Returns a URL pointing to a vector tile service that can be used in ArcGIS.
        """
        if self.servicer != "geoservices":
            raise ValueError(f"token is for '{self.servicer}', must be for 'geoservices'")
        if service_name is None:
            return f"{self.url}rest/services/{self.dataset}/VectorTileServer"
        else:
            return f"{self.url}rest/services/{service_name}/VectorTileServer"

    def get_image_service_url(self, service_name: str = None):
        """Gets a url to an GeoServices ImageService.

        Args:
            service_name: an optional service name to use in place of the dataset name

        Returns a URL pointing to an image service that can be used in ArcGIS.
        """
        if self.servicer != "geoservices":
            raise ValueError(f"token is for '{self.servicer}', must be for 'geoservices'")
        if service_name is None:
            return f"{self.url}rest/services/{self.dataset}/ImageServer"
        else:
            return f"{self.url}rest/services/{service_name}/ImageServer"

    def get_feature_service_url(self, service_name: str = None):
        """Gets a url to an GeoServices FeatureService.

        Args:
            service_name: an optional service name to use in place of the dataset name

        Returns a URL pointing to a feature service that can be used in ArcGIS.
        """
        if self.servicer != "geoservices":
            raise ValueError(f"token is for '{self.servicer}', must be for 'geoservices'")
        if service_name is None:
            return f"{self.url}rest/services/{self.dataset}/FeatureServer"
        else:
            return f"{self.url}rest/services/{service_name}/FeatureServer"

    def get_ogc_vector_tile_url(
        self,
        collection: str = None,
        tile_matrix_set_id: str = "WebMercatorQuad",
        tile_matrix_id: str = "z",
        row_name: str = "y",
        col_name: str = "x",
        format: str = "mvt",
    ) -> str:
        """Gets a url to an OGC API: Tiles service.

        Returns a URL pointing to a vector tile service that can be used in web mapping.
        """
        if format not in ["mvt", "pbf", "vectors.pbf"]:
            raise ValueError(
                f"format '{format}' is not supported, must be 'mvt', 'pbf', or 'vectors.pbf'"
            )
        return self._get_ogc_tile_url(
            format,
            collection,
            tile_matrix_set_id,
            tile_matrix_id,
            row_name,
            col_name,
        )

    def get_ogc_raster_tile_url(
        self,
        collection: str = None,
        tile_matrix_set_id: str = "WebMercatorQuad",
        tile_matrix_id: str = "z",
        row_name: str = "y",
        col_name: str = "x",
        format: str = "png",
        tile_path: str = "coverage/tiles",
    ) -> str:
        """Gets a url to an OGC API: Tiles service.

        Returns a URL pointing to a raster tile service that can be used in web mapping.
        """
        if format not in ["png", "jpg", "jpeg", "tif"]:
            raise ValueError(
                f"format '{format}' is not supported, must be 'png', 'jpg', 'jpeg', or 'tif'"
            )
        return self._get_ogc_tile_url(
            format,
            collection,
            tile_matrix_set_id,
            tile_matrix_id,
            row_name,
            col_name,
            tile_path=tile_path,
        )

    def _get_ogc_tile_url(
        self,
        format: str,
        collection: str = None,
        tile_matrix_set_id: str = "WebMercatorQuad",
        tile_matrix_id: str = "z",
        row_name: str = "y",
        col_name: str = "x",
        tile_path: str = "tiles",
    ) -> str:
        if self.servicer != "tiles":
            raise ValueError(f"token is for '{self.servicer}', must be for 'tiles'")
        if collection is None:
            collection = self.dataset

        suffix = "{" + tile_matrix_id + "}/{" + row_name + "}/{" + col_name + "}" + f".{format}"
        dataset_root = f"{self.url}collections/{collection}/{tile_path}/{tile_matrix_set_id}/"
        return f"{dataset_root}{suffix}"

    def get_feature_layer_url(self, layer_id: int = 0, service_name: str = None) -> str:
        """Gets a url to an GeoServices Feature Layer.

        Returns a URL pointing to a layer that can directly be used in ArcGIS.

        Args:
            layer_id: the layer ID to expose
            service_name: an optional service name to use in place of the dataset name

        Returns:
            a URL to to layer
        """
        return f"{self.get_feature_service_url(service_name=service_name)}/{layer_id}"

    feature_layer_url = deprecated("1.0.0", "Token.feature_layer_url")(get_feature_layer_url)

    def update_ttl(self, ttl: int):
        """Update the time to live of a token in redis.

        Args:
            ttl: the amount of seconds before the token should expire. Valid values are either -1,
                 representing an infinite token life, or n, where 0 < n <= 2147483647.

        Raises:
            requests.HTTPErrror for fault

        Note: If successful, nothing is returned.
        """
        raise_on_error(ted_client.patch(str(self.token) + "/" + str(ttl)))
        return

    def unshare(self):
        """Expires an active token created by the user, revoking access from anyone using the token.

        Raises:
            requests.HTTPErrror for fault

        .. Note::
            If successful, nothing is returned. Deleting a non-existent token does
            not raise an error.
        """
        raise_on_error(ted_client.delete(str(self.token)))
        return


def get_tokens() -> "Tokens":
    """Returns all active tokens created by a user.

    Raises:
        requests.HTTPErrror for fault
    """
    res = raise_on_error(ted_client.get(""))
    js = res.json()
    if js == {}:
        return Tokens()
    return Tokens([Token(**token) for token in js["tokens"]])


class Tokens(list):
    def __init__(self, tokens: List[Token] = []):
        super().__init__(tokens)
        self.lookup = defaultdict(list)
        for token in tokens:
            self.lookup[f"{token.project}:{token.dataset}"].append(token)

    def tokens_for(
        self, project: str, dataset: str, servicer: str = None, persistent_only: bool = False
    ) -> "Tokens":
        """Returns all active tokens created by a user for a specific project and dataset.

        Args:
            project: the project name
            dataset: the dataset name
            servicer: the servicer of the dataset (optional). If None, returns for all servicers
            persistent_only: if True, returns only tokens that do not expire

        Returns:
            a list of tokens
        """
        tokens = self.lookup[f"{project}:{dataset}"]
        if servicer is not None:
            tokens = Tokens([token for token in tokens if token.servicer == servicer])
        if persistent_only:
            tokens = Tokens([token for token in tokens if token.ttl == "-1"])
        return Tokens(tokens)
