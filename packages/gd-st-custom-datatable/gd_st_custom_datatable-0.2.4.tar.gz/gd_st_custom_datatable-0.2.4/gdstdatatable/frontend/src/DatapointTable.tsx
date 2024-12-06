import React, { useState, useEffect } from "react"
import { isEmpty, range } from "lodash"
import {
  DataEditor,
  EditableGridCell,
  GridCell,
  GridCellKind,
  GridColumn,
  Item
} from "@glideapps/glide-data-grid";
import { ArrowTable, ComponentProps, Streamlit, withStreamlitConnection } from "streamlit-component-lib"
import "@glideapps/glide-data-grid/dist/index.css";
import "@toast-ui/editor/dist/toastui-editor.css";
import { useExtraCells } from "@glideapps/glide-data-grid-cells";

// skip the first column without name (???)
const sourceColOffset = 1;

// cf https://github.com/glideapps/glide-data-grid/blob/main/packages/core/API.md
const portalStyle: React.CSSProperties = {
  position: "fixed",
  left: 0,
  top: 0,
  zIndex: 9999
};

interface TableData {
  columns: string[];
  cells: any[][];
}

interface ColumnSpec {
  name: string;
  grow?: number;
  width?: number;
  editable?: boolean;
}

function getTableData(table: ArrowTable): TableData {
  const rows = table.rows;
  const cols = table.columns;

  const cells = [];
  // skip header row
  for (let i = 1; i < rows; i++) {
    const row = [];
    for (let j = sourceColOffset; j < cols; j++) {
      const { content } = table.getCell(i, j);
      row.push(content);
    }
    cells.push(row);
  }

  return {
    columns: getColumns(table),
    cells: cells
  };
}

function getColumns(table: ArrowTable): string[] {
  return range(sourceColOffset, table.columns).map(columnIndex => {
    const { content } = table.getCell(0, columnIndex)
    return (content || '').toString()
  });
}

function getContentAt(row: number, colName: string, table: TableData): any {
  const colIndex = table.columns.indexOf(colName);
  return table.cells[row][colIndex];
}

function getGridColumns(columns: string[],
  addViewColumn: boolean,
  columnSpecs: ColumnSpec[]): GridColumn[] {
  if (!isEmpty(columnSpecs)) {
    columns = columnSpecs.map(c => c.name);
  }
  if (addViewColumn && !columns.includes("view")) {
    columns = columns.concat("view");
  }
  return columns
    .map(column => {
      const columnSpec = columnSpecs.find(c => c.name === column);
      if (columnSpec) {
        if (columnSpec.width) {
          return {
            title: column,
            width: columnSpec.width
          };
        } else {
          return {
            title: column,
            id: column,
            grow: columnSpec.grow
          };
        }
      } else {
        return { title: column, id: column };
      }
    });
}

// format value for sending to Streamlit
function formatValue(value: any): any {
  if (typeof value === "bigint") {
    return Number(value);
  } else {
    return value;
  }
}

function getGridCells(table: TableData,
  gridColumns: GridColumn[],
  columnSpecs: ColumnSpec[],
  addViewColumn: boolean,
  idColumn: string,
  onView: (id: any) => void,
): (item: Item) => GridCell {

  return function ([col, row]: Item): GridCell {
    const colName = gridColumns[col].title;
    const content = getContentAt(row, colName, table)
    const isColReadonly = !columnSpecs.some(c => c.editable);
    const id = getContentAt(row, idColumn, table)

    if ((colName === "view") && addViewColumn) {
      return {
        kind: GridCellKind.Custom,
        data: {
          kind: "button-cell",
          title: "view",
          onClick: () => onView(formatValue(id))
        },
        copyData: "view",
        allowOverlay: false,
        readonly: true
      };
    } else if (typeof (content) == 'boolean') {
      return {
        kind: GridCellKind.Boolean,
        data: content === true,
        allowOverlay: false,
        readonly: isColReadonly
      };
    } else {
      return {
        kind: GridCellKind.Text,
        data: (content || '').toString(),
        allowOverlay: true,
        readonly: isColReadonly,
        displayData: (content || '').toString(),
      };
    }
  };
}

const DatapointTable: React.FC<ComponentProps> = props => {
  const arrowTable: ArrowTable = props.args.data;
  const height: number = props.args.height ?? 34 * props.args.data.rows;
  const idColumn: string = props.args.id_column;
  const addViewColumn: boolean = props.args.add_view_column === true;
  const columnSpecs: ColumnSpec[] = props.args.column_specs ?? [];
  const width = props.args.width;
  const actionIdArg = props.args.actionId ?? 0;

  useEffect(() => {
    Streamlit.setFrameHeight(height);
  });

  const [actionId, setActionId] = useState(actionIdArg + 1);
  const [tableData, setTableData] = useState(getTableData(arrowTable));
  const gridColumns = getGridColumns(tableData.columns, addViewColumn, columnSpecs);

  const onCellEdited = (cell: Item, newValue: EditableGridCell) => {
    const [col, row] = cell;
    const colName = gridColumns[col].title;
    const colIndex = tableData.columns.indexOf(colName);

    tableData.cells[row][colIndex] = newValue.data;
    setTableData({ ...tableData });
    const id = getContentAt(row, idColumn, tableData);
    setActionId(actionId + 1);

    Streamlit.setComponentValue({
      action: "edit",
      id: formatValue(id),
      colName: colName,
      value: formatValue(newValue.data),
      actionId: actionId
    });
  };

  const onView = (id: any): void => {
    setActionId(actionId + 1);
    Streamlit.setComponentValue({
      action: "view",
      id: formatValue(id),
      actionId: actionId
    });
  }
  
  const { customRenderers } = useExtraCells();

  return <div>
    <div id="portal" style={portalStyle} />
    <DataEditor
      getCellContent={
        getGridCells(
          tableData,
          gridColumns,
          columnSpecs,
          addViewColumn,
          idColumn,
          onView)}
      columns={gridColumns}
      rows={tableData.cells.length}
      customRenderers={customRenderers}
      onCellEdited={onCellEdited}
      width={width}
      height={height}
    />
  </div>
}

export default withStreamlitConnection(DatapointTable)
