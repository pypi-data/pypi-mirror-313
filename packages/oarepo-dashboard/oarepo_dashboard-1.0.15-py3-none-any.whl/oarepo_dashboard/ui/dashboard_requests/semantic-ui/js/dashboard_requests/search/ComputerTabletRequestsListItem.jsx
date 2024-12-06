// This file is part of InvenioRDM
// Copyright (C) 2023 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/oarepo_dashboard";
import { default as RequestTypeIcon } from "@js/invenio_requests/components/RequestTypeIcon";
import React from "react";
import RequestTypeLabel from "@js/invenio_requests/request/RequestTypeLabel";
import RequestStatusLabel from "@js/invenio_requests/request/RequestStatusLabel";
import { Icon, Item } from "semantic-ui-react";
import PropTypes from "prop-types";
import { DateTime } from "luxon";

export const ComputerTabletRequestsListItem = ({
  result,
  updateQueryState,
  currentQueryState,
  detailsURL,
}) => {
  let creatorName = result.created_by.label;

  const getUserIcon = (receiver) => {
    return receiver?.is_ghost ? "user secret" : "users";
  };

  return (
    <Item
      key={result.id}
      className="computer tablet only rel-p-1 rel-mb-1 result-list-item request"
    >
      <div className="status-icon mr-10">
        <Item.Content verticalAlign="top">
          <Item.Extra>
            <RequestTypeIcon type={result.type} />
          </Item.Extra>
        </Item.Content>
      </div>
      <Item.Content>
        <Item.Extra>
          {result.type && <RequestTypeLabel type={result.type} />}
          {result.status && result.is_closed && (
            <RequestStatusLabel status={result.status_code} />
          )}
        </Item.Extra>
        {result?.topic?.status === "removed" ? (
          <Item.Header className="mt-5">
            {result?.title || result?.name}
          </Item.Header>
        ) : (
          <Item.Header className="truncate-lines-2  mt-10">
            <a className="header-link" href={detailsURL}>
              {result?.title || result?.name}
            </a>
          </Item.Header>
        )}
        <p className="rel-mt-1">
          {result.description || i18next.t("No description")}
        </p>
        <Item.Meta>
          <small>
            {i18next.t("Opened by {{creatorName}} on {{created}}.", {
              creatorName: creatorName,
              created: result.created,
              interpolation: { escapeValue: false },
            })}{" "}
            {result.receiver &&
              i18next.t("Recepient: {{receiver}}.", {
                receiver: result.receiver.label,
                interpolation: { escapeValue: false },
              })}
          </small>
          <small className="right floated">
            {result.receiver?.community &&
              result.expanded?.receiver.metadata.title && (
                <>
                  <Icon
                    className="default-margin"
                    name={getUserIcon(result.expanded?.receiver)}
                  />
                  <span className="ml-5">
                    {result.expanded?.receiver.metadata.title}
                  </span>
                </>
              )}
            {result.expires_at && (
              <span>
                {i18next.t("Expires at: {{- expiringDate}}", {
                  expiringDate: DateTime.fromISO(
                    result.expires_at
                  ).toLocaleString(i18next.language),
                })}
              </span>
            )}
          </small>
        </Item.Meta>
      </Item.Content>
    </Item>
  );
};

ComputerTabletRequestsListItem.propTypes = {
  result: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  detailsURL: PropTypes.string.isRequired,
};
