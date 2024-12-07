/*
 * Copyright (C) 2024 CESNET z.s.p.o.
 *
 * oarepo-requests is free software; you can redistribute it and/or
 * modify it under the terms of the MIT License; see LICENSE file for more
 * details.
 */
import React, { useState, useCallback, useRef } from "react";
import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { Message, Icon } from "semantic-ui-react";
import { useMutation } from "@tanstack/react-query";
import {
  useCallbackContext,
  REQUEST_TYPE,
  WarningMessage,
  RequestCommentInput,
  ConfirmationModalCancelButton,
  ConfirmationModalConfirmButton,
} from "@js/oarepo_requests_common";

/**
 * @typedef {import("semantic-ui-react").ConfirmProps} ConfirmProps
 */

const createConfirmDialogProps = (requestOrRequestType) => ({
  header: `${i18next.t("Create request")} (${requestOrRequestType.name})`,
  confirmButton: (
    <ConfirmationModalConfirmButton negative content={i18next.t("Proceed")} />
  ),
  content: (
    <WarningMessage
      message={i18next.t(
        "Are you sure you wish to proceed? After this request is accepted, it will not be possible to reverse the action."
      )}
    />
  ),
});

const submitConfirmDialogProps = (requestOrRequestType) => ({
  header: `${i18next.t("Submit request")} (${requestOrRequestType.name})`,
  confirmButton: (
    <ConfirmationModalConfirmButton negative content={i18next.t("Proceed")} />
  ),
  content: (
    <WarningMessage
      message={i18next.t(
        "Are you sure you wish to proceed? After this request is accepted, it will not be possible to reverse the action."
      )}
    />
  ),
});

const cancelConfirmDialogProps = (requestOrRequestType) => ({
  header: `${i18next.t("Cancel request")} (${requestOrRequestType.name})`,
  confirmButton: (
    <ConfirmationModalConfirmButton
      content={i18next.t("Cancel request")}
      negative
    />
  ),
});

const acceptConfirmDialogProps = (requestOrRequestType, dangerous) => ({
  header: `${i18next.t("Accept request")} (${requestOrRequestType.name})`,
  confirmButton: (
    <ConfirmationModalConfirmButton
      positive={!dangerous}
      negative={dangerous}
      content={i18next.t("Accept")}
    />
  ),
  content: dangerous && (
    <WarningMessage
      message={i18next.t(
        "This action is irreversible. Are you sure you wish to accept this request?"
      )}
    />
  ),
});

const declineConfirmDialogProps = (
  requestOrRequestType,
  comment,
  handleChange
) => {
  return {
    header: `${i18next.t("Decline request")} (${requestOrRequestType.name})`,
    confirmButton: (
      <ConfirmationModalConfirmButton content={i18next.t("Decline")} negative />
    ),
    content: (
      <div className="content">
        <RequestCommentInput comment={comment} handleChange={handleChange} />
        <Message>
          <Icon name="info circle" className="text size large" />
          <span>
            {i18next.t(
              "It is highly recommended to provide an explanation for the rejection of the request. Note that it is always possible to provide explanation later on the request timeline."
            )}
          </span>
        </Message>
      </div>
    ),
  };
};

export const useConfirmDialog = (requestOrRequestType) => {
  const [confirmDialogProps, setConfirmDialogProps] = useState({
    open: false,
    content: i18next.t("Are you sure?"),
    cancelButton: <ConfirmationModalCancelButton />,
    confirmButton: <ConfirmationModalConfirmButton />,
    onCancel: () =>
      setConfirmDialogProps((props) => ({ ...props, open: false })),
    onConfirm: () =>
      setConfirmDialogProps((props) => ({ ...props, open: false })),
  });
  const [comment, setComment] = useState("");
  const commentRef = useRef(comment);

  const handleChange = (event, value) => {
    setComment(value);
    commentRef.current = value;
  };
  const confirmAction = useCallback(
    (onConfirm, requestActionType, extraData) => {
      const dangerous = extraData?.dangerous;
      const baseConfirmDialogProps = {
        open: true,
        content: dangerous ? <WarningMessage /> : i18next.t("Are you sure?"),
        onConfirm: () => {
          setConfirmDialogProps((props) => ({ ...props, open: false }));
          onConfirm(commentRef.current);
        },
        onCancel: () => {
          setConfirmDialogProps((props) => ({ ...props, open: false }));
          setComment("");
        },
      };

      let caseSpecificProps = {};
      switch (requestActionType) {
        case REQUEST_TYPE.CREATE:
          caseSpecificProps = createConfirmDialogProps(requestOrRequestType);
          break;
        case REQUEST_TYPE.SUBMIT:
          caseSpecificProps = submitConfirmDialogProps(requestOrRequestType);
          break;
        case REQUEST_TYPE.CANCEL:
          caseSpecificProps = cancelConfirmDialogProps(requestOrRequestType);
          break;
        case REQUEST_TYPE.ACCEPT:
          caseSpecificProps = acceptConfirmDialogProps(
            requestOrRequestType,
            dangerous
          );
          break;
        case REQUEST_TYPE.DECLINE:
          caseSpecificProps = declineConfirmDialogProps(
            requestOrRequestType,
            comment,
            handleChange
          );
          break;
        default:
          break;
      }

      setConfirmDialogProps((props) => ({
        ...props,
        ...baseConfirmDialogProps,
        ...caseSpecificProps,
      }));
    },
    [comment, requestOrRequestType]
  );

  return { confirmDialogProps, confirmAction };
};

export const useAction = ({
  action,
  requestOrRequestType,
  formik,
  modalControl,
} = {}) => {
  const { onBeforeAction, onAfterAction, onActionError } = useCallbackContext();
  return useMutation(
    async (values) => {
      if (onBeforeAction) {
        const shouldProceed = await onBeforeAction(
          formik,
          modalControl,
          requestOrRequestType
        );
        if (!shouldProceed) {
          modalControl?.closeModal();
          throw new Error("Could not proceed with the action.");
        }
      }
      const formValues = { ...formik?.values };
      if (values) {
        formValues.payload.content = values;
      }
      return action(requestOrRequestType, formValues);
    },
    {
      onError: (e, variables) => {
        if (onActionError) {
          onActionError(
            e,
            variables,
            formik,
            modalControl,
            requestOrRequestType
          );
        } else if (e?.response?.data?.errors) {
          formik?.setFieldError(
            "api",
            i18next.t(
              "The request could not be created due to validation errors. Please correct the errors and try again."
            )
          );
          setTimeout(() => {
            modalControl?.closeModal();
          }, 2500);
        } else {
          formik?.setFieldError(
            "api",
            i18next.t(
              "The action could not be executed. Please try again in a moment."
            )
          );
          setTimeout(() => {
            modalControl?.closeModal();
          }, 2500);
        }
      },
      onSuccess: (data, variables) => {
        if (onAfterAction) {
          onAfterAction(
            data,
            variables,
            formik,
            modalControl,
            requestOrRequestType
          );
        }
        const redirectionURL = data?.data?.links?.topic_html;
        modalControl?.closeModal();

        if (redirectionURL) {
          window.location.href = redirectionURL;
        } else {
          // TODO: some requests after they complete no longer have a topic_html,
          // so redirecting to dashboard instead
          window.location.href = "/me/records/";
          // fetchNewRequests?.();
        }
      },
    }
  );
};
