import React from "react";
import { Button, Confirm } from "semantic-ui-react";
import { RequestModal, CreateRequestModalContent } from ".";
import {
  DirectCreateAndSubmit,
  ConfirmModalContextProvider,
} from "@js/oarepo_requests_common";
import PropTypes from "prop-types";

export const CreateRequestButton = ({
  requestType,
  isMutating,
  buttonIconProps,
  header,
}) => {
  const { dangerous, has_form: hasForm } = requestType;
  const needsDialog = dangerous || hasForm;

  if (!hasForm && dangerous) {
    return (
      <ConfirmModalContextProvider requestOrRequestType={requestType}>
        {({ confirmDialogProps }) => (
          <>
            <DirectCreateAndSubmit
              requestType={requestType}
              requireConfirmation={dangerous}
              isMutating={isMutating}
            />
            <Confirm
              {...confirmDialogProps}
              className="requests dangerous-action-confirmation-modal"
            />
          </>
        )}
      </ConfirmModalContextProvider>
    );
  }

  if (!hasForm && !dangerous) {
    return (
      <ConfirmModalContextProvider requestOrRequestType={requestType}>
        {({ confirmDialogProps }) => (
          <>
            <DirectCreateAndSubmit
              requestType={requestType}
              requireConfirmation={false}
              isMutating={isMutating}
            />
            <Confirm
              {...confirmDialogProps}
              className="requests dangerous-action-confirmation-modal"
            />
          </>
        )}
      </ConfirmModalContextProvider>
    );
  }

  if (needsDialog) {
    return (
      <RequestModal
        requestType={requestType}
        header={header}
        requestCreationModal
        trigger={
          <Button
            className={`requests request-create-button ${requestType.type_id}`}
            fluid
            title={header}
            content={header}
            disabled={isMutating > 0}
            {...buttonIconProps}
          />
        }
        ContentComponent={CreateRequestModalContent}
      />
    );
  }

  return null;
};

CreateRequestButton.propTypes = {
  requestType: PropTypes.object,
  isMutating: PropTypes.number.isRequired,
  buttonIconProps: PropTypes.object,
  header: PropTypes.string.isRequired,
};
