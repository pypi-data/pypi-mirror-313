import React from "react";
import { Button, Icon } from "semantic-ui-react";
import PropTypes from "prop-types";
import { useFormikContext } from "formik";
import {
  useConfirmModalContext,
  useModalControlContext,
  useAction,
} from "@js/oarepo_requests_common";

export const RequestActionButton = ({
  requestOrRequestType,
  extraData,
  isMutating,
  iconName,
  action,
  buttonLabel,
  requireConfirmation,
  requestActionName,
  ...uiProps
}) => {
  const formik = useFormikContext();
  const { confirmAction } = useConfirmModalContext();
  const modalControl = useModalControlContext();
  const { isLoading, mutate: requestAction } = useAction({
    action,
    requestOrRequestType: requestOrRequestType,
    formik,
    modalControl,
  });

  const handleClick = () => {
    if (requireConfirmation) {
      confirmAction(
        (value) => requestAction(value),
        requestActionName,
        extraData
      );
    } else {
      requestAction();
    }
  };

  return (
    <Button
      title={buttonLabel}
      onClick={() => handleClick()}
      className="requests request-accept-button"
      icon
      labelPosition="left"
      loading={isLoading}
      disabled={isMutating > 0}
      {...uiProps}
    >
      <Icon name={iconName} />
      {buttonLabel}
    </Button>
  );
};

RequestActionButton.propTypes = {
  requestOrRequestType: PropTypes.object,
  extraData: PropTypes.object,
  isMutating: PropTypes.number,
  iconName: PropTypes.string,
  action: PropTypes.func,
  buttonLabel: PropTypes.string,
  requireConfirmation: PropTypes.bool,
  requestActionName: PropTypes.string,
};

export default RequestActionButton;
