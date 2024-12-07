import React, { useState } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { Button, Message, Form } from "semantic-ui-react";
import { RequestCommentInput } from "@js/oarepo_requests_common";

export const CommentSubmitForm = ({ commentSubmitMutation }) => {
  const {
    mutate: submitComment,
    isLoading,
    isError,
    reset: resetSendCommentMutation,
  } = commentSubmitMutation;

  const [comment, setComment] = useState({
    payload: { content: "", format: "html" },
  });

  const handleCommentChange = (event, value) => {
    setComment({
      payload: {
        content: value,
        format: "html",
      },
    });
  };

  const handleFormReset = () => {
    setComment({
      payload: { content: "", format: "html" },
    });
  };

  const handleCommentSubmit = () => {
    submitComment(comment, {
      onSuccess: () => {
        handleFormReset();
      },
      onError: () => {
        setTimeout(() => resetSendCommentMutation(), 3000);
      },
    });
  };

  return (
    <Form className="ui form">
      <RequestCommentInput
        comment={comment.payload.content}
        handleChange={handleCommentChange}
      />
      {isError && (
        <Message negative>
          <Message.Header>
            {i18next.t(
              "Comment was not submitted successfully. Please try again in a moment."
            )}
          </Message.Header>
        </Message>
      )}
      <Button
        size="tiny"
        floated="right"
        primary
        icon="send"
        type="button"
        className="rel-mt-1"
        labelPosition="left"
        loading={isLoading}
        disabled={isLoading || !comment.payload.content}
        content={i18next.t("Leave comment")}
        onClick={handleCommentSubmit}
      />
    </Form>
  );
};

CommentSubmitForm.propTypes = {
  commentSubmitMutation: PropTypes.object.isRequired,
};
