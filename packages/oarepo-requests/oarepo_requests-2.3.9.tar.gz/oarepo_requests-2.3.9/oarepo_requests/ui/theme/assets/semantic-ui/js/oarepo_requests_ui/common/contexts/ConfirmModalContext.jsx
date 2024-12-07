import React, { createContext, useContext } from "react";
import { useConfirmDialog } from "@js/oarepo_requests_common";
import PropTypes from "prop-types";

const ConfirmModalContext = createContext();

export const ConfirmModalContextProvider = ({
  children,
  requestOrRequestType,
}) => {
  const confirmDialogStateAndHelpers = useConfirmDialog(requestOrRequestType);
  return (
    <ConfirmModalContext.Provider value={confirmDialogStateAndHelpers}>
      {typeof children === "function"
        ? children(confirmDialogStateAndHelpers)
        : children}
    </ConfirmModalContext.Provider>
  );
};

ConfirmModalContextProvider.propTypes = {
  children: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
  requestOrRequestType: PropTypes.object,
};

export const useConfirmModalContext = () => {
  const context = useContext(ConfirmModalContext);
  if (!context) {
    console.warn(
      "useConfirmModalContext must be used inside ConfirmModalContext.Provider"
    );
  }
  return context;
};
