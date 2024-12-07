import React from "react";
import PropTypes from "prop-types";
import { Button } from "semantic-ui-react";
import { RequestModal, RequestModalContent } from ".";
import { useRequestContext } from "@js/oarepo_requests_common";
import { useIsMutating } from "@tanstack/react-query";

/**
 * @typedef {import("../types").Request} Request
 */

/**
 * @param {{ requests: Request[] }} props
 */
export const RequestList = ({ requests }) => {
  const { requestButtonsIconsConfig } = useRequestContext();
  const isMutating = useIsMutating();
  return requests.map((request) => {
    const buttonIconProps = requestButtonsIconsConfig[request.status_code];
    const header = request?.stateful_name || request?.name;
    return (
      <RequestModal
        key={request.id}
        request={request}
        requestType={request}
        header={header}
        requestCreationModal={false}
        trigger={
          <Button
            className={`requests request-reply-button ${request.type} ${request.type}-${request.status_code}`}
            fluid
            title={header}
            content={header}
            disabled={isMutating > 0}
            {...buttonIconProps}
          />
        }
        ContentComponent={RequestModalContent}
      />
    );
  });
};

RequestList.propTypes = {
  requests: PropTypes.array.isRequired,
};
