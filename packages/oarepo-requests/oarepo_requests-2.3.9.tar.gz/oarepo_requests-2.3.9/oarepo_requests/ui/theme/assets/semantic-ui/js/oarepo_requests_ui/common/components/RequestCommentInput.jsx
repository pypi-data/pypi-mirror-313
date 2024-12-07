import React from "react";
import { RichEditor } from "react-invenio-forms";
import sanitizeHtml from "sanitize-html";
import PropTypes from "prop-types";
import { useQuery } from "@tanstack/react-query";
import { httpApplicationJson } from "@js/oarepo_ui";

export const RequestCommentInput = ({
  comment,
  handleChange,
  initialValue,
}) => {
  // when focused move the cursor at the end of any existing content
  const handleFocus = (event, editor) => {
    editor.selection.select(editor.getBody(), true);
    editor.selection.collapse(false);
  };

  // TODO: there is no appropriate URL to call here. I think this one is the safest, because we know it exists and it does
  // not rely on external library (like those that contain /me that are from dashboard). To be discussed how to handle this appropriately.
  // maybe some link that lives in oarepo ui and that can universaly provide allowed tags and attributes
  const { data } = useQuery(
    ["allowedHtmlTagsAttrs"],
    () => httpApplicationJson.get(`/requests/configs/publish_draft`),
    {
      refetchOnWindowFocus: false,
      staleTime: Infinity,
    }
  );

  const allowedHtmlAttrs = data?.data?.allowedHtmlAttrs;
  const allowedHtmlTags = data?.data?.allowedHtmlTags;
  return (
    <RichEditor
      initialValue={initialValue}
      inputValue={comment}
      editorConfig={{
        auto_focus: true,
        min_height: 100,
        toolbar:
          "blocks | bold italic | bullist numlist | outdent indent | undo redo",
      }}
      onEditorChange={(event, editor) => {
        const cleanedContent = sanitizeHtml(editor.getContent(), {
          allowedTags: allowedHtmlTags,
          allowedAttributes: allowedHtmlAttrs,
        });

        handleChange(event, cleanedContent);
      }}
      onFocus={handleFocus}
    />
  );
};

RequestCommentInput.propTypes = {
  comment: PropTypes.string,
  handleChange: PropTypes.func,
  initialValue: PropTypes.string,
};

RequestCommentInput.defaultProps = {
  initialValue: "",
};
