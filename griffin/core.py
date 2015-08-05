# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function


import ramlfications


from .utils import OrderedDefaultDict as defaultdict  # NOQA


class APIContext(object):
    """
    Context object of the parsed API.

    :param api: The API parsed by \
        `ramlfications <https://ramlfications.readthedocs.org/en/latest>`_.
    """
    def __init__(self, api):
        self.api = api
        self.metadata = self._set_metadata()
        self.groupings, self.endpoints = self._set_endpoints()

    @staticmethod
    def _create_anchor(node):
        """
        Cleans up the endpoint.path attribute to create an ``href`` anchor.

        :param obj node: resource node object
        :rtype: str
        """
        anchor = node.path.lstrip("/")
        anchor = anchor.replace("/", "-")
        anchor = anchor.replace("_", "-")
        anchor = anchor.replace("{", "")
        anchor = anchor.replace("}", "")

        if node.method:
            anchor = "-".join([node.method, anchor])
        return anchor

    @staticmethod
    def _get_parent_node(node):
        """
        Returns the parent node of an endpoint, and strips the trailing
        ``/``.  Default grouping order.

        :param obj node: resource node object
        :ret: parent name of the node
        :rtype: str
        """
        if node.parent:
            return APIContext._get_parent_node(node.parent)
        return node.name.lstrip("/")

    @staticmethod
    def _create_curl_example(node):
        """
        Returns complete cURL string using the resource node examples.
        :param obj node: resource node object
        :ret: example cURL command
        :rtype: str
        """
        curl_url = node.absolute_uri
        q_string = ""
        f_string = ""
        h_string = ""
        if node.query_params:
            query_p = [(q.name, q.example) for q in node.query_params]
            for q in query_p:
                q_string += "{0}={1}".format(q[0], q[1])
        if node.form_params:
            form_p = [(f.name, f.example)for f in node.form_params]
            for f in form_p:
                f_string += " -d {0}={1}".format(f[0], f[1])
        if node.uri_params:
            uri_p = [(u.name, u.example) for u in node.uri_params if u.example]
            for u in uri_p:
                curl_url = curl_url.replace("{" + u[0] + "}", str(u[1]))
        if node.headers:
            headers = [(h.name, h.example) for h in node.headers]
            for h in headers:
                h_string += ' -H "{0}: {1}"'.format(h[0], h[1])

        if q_string:
            curl_url = curl_url + "?" + q_string

        if node.secured_by:
            secured = ' -H "Authorization: Bearer A-v@1id-o@uth-t0k3n"'
            curl_url = '"{0}"'.format(curl_url) + secured

        if h_string:
            curl_url = curl_url + h_string

        if f_string:
            curl_url = curl_url + f_string

        # what if there are multiple bodies?
        if node.body:
            body = node.body[0].example
            body_mime = node.body[0].mime_type
            b_header = ' -H "Content-Type: {0}"'.format(body_mime)
            b_data = ' --data "{0}"'.format(body)
            curl_url = curl_url + b_header + b_data

        return curl_url

    @staticmethod
    def _sort_resp_codes(responses):
        """
        Returns response codes in numeric order.

        :param list responses: list of resource-supported responses
        :ret: ordered ``list`` of resource param objects
        """
        try:
            return sorted(responses, key=lambda k: k)
        except TypeError:
            return responses

    @staticmethod
    def _sort_required(params):
        """
        Returns the parameters by with required on top, followed by
        order within the RAML file.

        :param list params: list of resource param objects
        :ret: ordered ``list`` of resource param objects
        """
        if params is not None:
            ordered_params = []
            for p in params:
                if p.required:
                    ordered_params.append(p)
            for p in params:
                if p not in ordered_params:
                    ordered_params.append(p)
            return ordered_params
        return params

    def _set_metadata(self):
        """
        Returns metadata about the API

        :param obj api: parsed RAML API
        :rtype: ``dict``
        """
        return dict(title=self.api.title,
                    version=self.api.version,
                    protocols=self.api.protocols,
                    docs=self.api.documentation,
                    uri=self.api.base_uri,
                    b_params=self.api.base_uri_params,
                    u_params=self.api.uri_params,
                    traits=self.api.traits,
                    types=self.api.resource_types,
                    secured=self.api.secured_by,
                    sec_schemes=self.api.security_schemes,
                    media_type=self.api.media_type)

    def _set_endpoints(self):
        """
        Parses API object into dictionaries for each endpoint and their
        respective groupings.

        :param obj api: parsed RAML API
        """
        res = self.api.resources

        groupings = defaultdict(list)
        endpoints = []
        for r in res:
            anchor = self._create_anchor(r)
            parent = self._get_parent_node(r)
            curl_url = self._create_curl_example(r)
            if r.description.raw:
                desc = r.description.html
            else:
                desc = ''
            endpoint = dict(anchor=anchor,
                            curl=curl_url,
                            display_name=r.display_name,
                            name=r.name,
                            path=r.path,
                            method=r.method,
                            media_type=r.media_type,
                            description=desc,
                            headers=r.headers,
                            body=r.body,
                            resp=self._sort_resp_codes(r.responses),
                            protocols=r.protocols,
                            q_params=self._sort_required(r.query_params),
                            f_params=self._sort_required(r.form_params),
                            u_params=self._sort_required(r.uri_params),
                            secured=r.secured_by)
            endpoints.append(endpoint)
            groupings[parent].append(endpoint)

        return groupings, endpoints

    def __repr__(self):
        return self.api.title


def create_context(ramlfile, ramlconfig=None):
    """
    Returns context to populate templates.

    :param str ramlfile:  RAML file to parse
    :param str ramlconfig: config file for RAML (see ``ramlfications`` \
        `docs <https://ramlfications.readthedocs.org/en/latest/config.html>`_)
    :rtype: :py:class:`.APIContext` object
    """
    api = ramlfications.parse(ramlfile, ramlconfig)

    return APIContext(api)
