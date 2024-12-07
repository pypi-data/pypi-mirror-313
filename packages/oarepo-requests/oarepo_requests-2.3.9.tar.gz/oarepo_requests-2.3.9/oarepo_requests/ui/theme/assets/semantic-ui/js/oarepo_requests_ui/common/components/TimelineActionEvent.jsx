import React from "react";
import {
  getRequestStatusIcon,
  getFeedMessage,
} from "@js/oarepo_requests_common";
import PropTypes from "prop-types";
import { Icon, Feed } from "semantic-ui-react";
import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { toRelativeTime, Image } from "react-invenio-forms";

export const TimelineActionEvent = ({ event }) => {
  const createdBy = event?.expanded?.created_by;
  const creatorLabel = createdBy?.username || createdBy?.email;
  const eventIcon = getRequestStatusIcon(event.payload.event);
  const feedMessage = getFeedMessage(event.payload.event);

  return (
    <div className="requests action-event-container">
      <Feed.Event>
        <div className="action-event-vertical-line"></div>
        <Feed.Content>
          <Feed.Summary className="flex align-items-center">
            <div className="flex align-items-center justify-center">
              <Icon
                className="requests action-event-icon"
                name={eventIcon?.name}
                color={eventIcon?.color}
              />
            </div>
            <div className="requests action-event-avatar inline-block">
              <Image
                src={createdBy?.links?.avatar}
                alt={i18next.t("User avatar")}
              />
            </div>
            <b className="ml-5">{creatorLabel}</b>
            <Feed.Date>
              {feedMessage} {toRelativeTime(event.updated, i18next.language)}
            </Feed.Date>
          </Feed.Summary>
        </Feed.Content>
      </Feed.Event>
    </div>
  );
};

TimelineActionEvent.propTypes = {
  event: PropTypes.object,
};
