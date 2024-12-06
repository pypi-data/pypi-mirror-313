import React from "react";
import { Label } from "semantic-ui-react";
import { i18next } from "@translations/oarepo_dashboard";

export const LabelTypeEditRecord = (props) => (
  <Label horizontal size="small">
    {i18next.t("Edit record")}
  </Label>
);

export const LabelTypeDeleteRecord = (props) => (
  <Label horizontal size="small">
    {i18next.t("Delete record")}
  </Label>
);

export const LabelTypePublishRecord = (props) => (
  <Label horizontal size="small">
    {i18next.t("Publish record")}
  </Label>
);

export const LabelTypeRecordNewVersion = (props) => (
  <Label horizontal size="small">
    {i18next.t("Create new version of record")}
  </Label>
);

export const LabelTypeAssignDoi = (props) => (
  <Label horizontal size="small">
    {i18next.t("Assign DOI")}
  </Label>
);
