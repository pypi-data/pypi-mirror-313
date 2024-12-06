# custom-datatable

`custom-datatable` is a custom streamlit component showing a [glide data grid](https://grid.glideapps.com/).

|   arg name      |      description             |
| --------------- | ---------------------------- |
| id_column        | column of the id for actions |
| height          | frame height                 |
| editables       | list of editable columns     |
| hides           | list of hidden columns       |
| add_view_column | add a view column            |
| column_width    | dict of column widths        |

# Quick use

In `custom_datatable/frontend` run:

```
npm install
npm start
```

In root folder:

```
poetry install
poetry shell
streamlit run custom_datatable/example.py
```