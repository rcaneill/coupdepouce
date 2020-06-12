schema_ajout_cdp = {
  "title": "Titre de l'activité",
  "headerTemplate": "{{ self.title }}",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "title": "Titre de l'activité"
    },
    "data": {
      "type": "array",
      "title": "Questions",
      "items": {
        "type": "object",
        "title": "Question",
        "headerTemplate": "{{ self.titre }}",
        "properties": {
          "titre": {
            "title": "Titre / numéro de la question",
            "type": "string"
          },
          "cdp": {
            "title": "Coup de pouce",
            "type": "array",
            "items": {
              "type": "string",
              "format": "textarea",
              "title": "coup de pouce sous partie",
              "headerTemplate": "{{ i1 }} "
            }
          }
        }
      }
    }
  }
}
