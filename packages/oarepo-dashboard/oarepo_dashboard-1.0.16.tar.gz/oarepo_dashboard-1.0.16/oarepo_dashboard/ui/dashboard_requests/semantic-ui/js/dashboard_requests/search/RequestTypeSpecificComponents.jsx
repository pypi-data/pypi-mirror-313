import {
  LabelTypeEditRecord,
  LabelTypeDeleteRecord,
  LabelTypePublishRecord,
  LabelTypeRecordNewVersion,
  LabelTypeAssignDoi,
} from "./labels/TypeLabels";
import {
  PublishRecordIcon,
  DeleteRecordIcon,
  EditRecordIcon,
  RecordNewVersionIcon,
  AssignDoiIcon,
} from "./icons/TypeIcons";

export const requestTypeSpecificComponents = {
  [`RequestTypeLabel.layout.edit_published_record`]: LabelTypeEditRecord,
  [`RequestTypeLabel.layout.delete_published_record`]: LabelTypeDeleteRecord,
  [`RequestTypeLabel.layout.publish_draft`]: LabelTypePublishRecord,
  [`RequestTypeLabel.layout.new_version`]: LabelTypeRecordNewVersion,
  [`RequestTypeLabel.layout.assign_doi`]: LabelTypeAssignDoi,
  [`InvenioRequests.RequestTypeIcon.layout.edit_published_record`]:
    EditRecordIcon,
  [`InvenioRequests.RequestTypeIcon.layout.delete_published_record`]:
    DeleteRecordIcon,
  [`InvenioRequests.RequestTypeIcon.layout.publish_draft`]: PublishRecordIcon,
  PublishRecordIcon,
  [`InvenioRequests.RequestTypeIcon.layout.new_version`]: RecordNewVersionIcon,
  [`InvenioRequests.RequestTypeIcon.layout.assign_doi`]: AssignDoiIcon,
};
