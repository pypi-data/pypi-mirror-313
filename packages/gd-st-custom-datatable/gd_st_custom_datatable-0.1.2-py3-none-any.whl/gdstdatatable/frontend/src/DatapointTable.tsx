import React, { useState, useEffect } from "react"
import { range } from "lodash"
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

interface ColumnWidth {
  [index: string]: number;
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
  hides: string[], 
  addViewColumn: boolean,
  columnWidth: ColumnWidth): GridColumn[] {
  if (addViewColumn) {
    columns = columns.concat("view");
  }
  return columns
    .filter(column => !hides.includes(column))
    .map(column => {
      const width = columnWidth[column] ?? 100;
      return { title: column, width: width }
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
  editables: string[],
  addViewColumn: boolean,
  idColumn: string): (item: Item) => GridCell {

  return function ([col, row]: Item): GridCell {
    const colName = gridColumns[col].title;
    const content = getContentAt(row, colName, table)
    const isColReadonly = !editables.includes(colName);
    const id = getContentAt(row, idColumn, table)

    if ((colName === "view") && addViewColumn) {
      return {
        kind: GridCellKind.Custom,
        data: {
          kind: "button-cell",
          title: "view",
          onClick: () => {
            Streamlit.setComponentValue({ action: "view", id: formatValue(id) });
          }
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
  const editables: string[] = props.args.editables ?? [];
  const hides: string[] = props.args.hides ?? [];
  const idColumn: string = props.args.id_column
  const addViewColumn: boolean = props.args.add_view_column === true
  const columnWidth: ColumnWidth = props.args.column_width ?? {};

  useEffect(() => {
    Streamlit.setFrameHeight(height);
  });

  const [tableData, setTableData] = useState(getTableData(arrowTable))

  const onCellEdited = React.useCallback((cell: Item, newValue: EditableGridCell) => {
    const [col, row] = cell;
    tableData.cells[row][col] = newValue.data;
    setTableData({ ...tableData });
    const colName = tableData.columns[col];
    const id = getContentAt(row, idColumn, tableData)

    Streamlit.setComponentValue({
      action: "edit",
      id: formatValue(id),
      colName: colName,
      value: formatValue(newValue.data)
    });
  }, [tableData, idColumn]);

  const { customRenderers } = useExtraCells();
  const gridColumns = getGridColumns(tableData.columns, hides, addViewColumn, columnWidth);
  return <div>
    <div id="portal" style={portalStyle} />
    <DataEditor
      getCellContent={
        getGridCells(
          tableData,
          gridColumns,
          editables,
          addViewColumn,
          idColumn)}
      columns={gridColumns}
      rows={tableData.cells.length}
      customRenderers={customRenderers}
      onCellEdited={onCellEdited}
    />
  </div>
}

export default withStreamlitConnection(DatapointTable)
