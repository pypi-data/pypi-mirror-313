import React from "react";
import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { Icon, List } from "semantic-ui-react";
import _has from "lodash/has";
import _truncate from "lodash/truncate";
import { getRequestStatusIcon } from "@js/oarepo_requests_common";
import PropTypes from "prop-types";

export const SideRequestInfo = ({ request }) => {
  const statusIcon = getRequestStatusIcon(request?.status_code);
  return (
    <List horizontal relaxed divided size="small">
      <List.Item>
        <List.Header as="h3">{i18next.t("Creator")}</List.Header>
        <List.Content>
          <Icon name="user circle outline" />
          <span>
            {_has(request, "links.created_by_html") ? (
              <a
                href={request.links.created_by_html}
                target="_blank"
                rel="noreferrer"
              >
                {request.created_by.label}
              </a>
            ) : (
              request.created_by?.label
            )}
          </span>
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Header as="h3">{i18next.t("Receiver")}</List.Header>
        <List.Content>
          <Icon name="mail outline" />
          <span>
            {_has(request, "links.receiver_html") ? (
              <a
                href={request.links.receiver_html}
                target="_blank"
                rel="noreferrer"
              >
                {request?.receiver?.label}
              </a>
            ) : (
              request?.receiver?.label
            )}
          </span>
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Header as="h3">{i18next.t("Status")}</List.Header>
        <List.Content>
          {statusIcon && (
            <Icon name={statusIcon.name} color={statusIcon.color} />
          )}
          <span>{request.status}</span>
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Header as="h3">{i18next.t("Created")}</List.Header>
        <List.Content>{request.created}</List.Content>
      </List.Item>
      {request?.links?.topic_html && (
        <List.Item>
          <List.Header as="h3">{i18next.t("Topic")}</List.Header>
          <List.Content>
            <a href={request.links.topic_html} target="_blank" rel="noreferrer">
              {request?.topic?.label
                ? _truncate(request?.topic?.label, {
                    length: 350,
                  })
                : i18next.t("Request topic")}
            </a>
          </List.Content>
        </List.Item>
      )}
    </List>
  );
};

SideRequestInfo.propTypes = {
  request: PropTypes.object,
};
