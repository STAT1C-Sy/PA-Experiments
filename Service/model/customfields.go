package model

type CustomFieldValueOptions struct {
	Value       string `json:"value"`
	DisplayText string `json:"displayText"`
}

type ValueoptionsResponse []CustomFieldValueOptions

//copied from customfieldsservice
type ConfigCustomField struct {
	CustomFieldValues      []ConfigCustomFieldValue `json:"customFieldValues"`
	DataType               string                   `json:"dataType"`
	DependencyFieldID      string                   `json:"dependencyFieldId"`
	DependencyType         string                   `json:"dependencyType"`
	DependencyValues       []string                 `json:"dependencyValues"`
	DisplayAtEnd           bool                     `json:"displayAtEnd"`
	DisplayAtStart         bool                     `json:"displayAtStart"`
	DisplayTitle           string                   `json:"displayTitle"`
	ID                     string                   `json:"uuid"`
	MaxLength              int                      `json:"maxLength"`
	MinLength              int                      `json:"minLength"`
	Name                   string                   `json:"name"`
	Required               bool                     `json:"required"`
	TotalValues            int                      `json:"totalValues"`
	AttributeType          string                   `json:"attributeType"`
	DisplayForRegularTrips bool                     `json:"displayForRegularTrips"`
}

type ConfigCustomFieldValue struct {
	ID    string `json:"id"`
	Order int    `json:"order"`
	Text  string `json:"text"`
	Value string `json:"value"`
}

type CustomFieldServiceResponse []ConfigCustomField
