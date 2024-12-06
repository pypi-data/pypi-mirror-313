import React, { useMemo, useEffect, useState, Fragment } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  useTable,
  useGlobalFilter,
  useSortBy,
  usePagination,
  useFilters,
  useAsyncDebounce,
  useRowSelect,
} from "react-table";
import {
  Pagination,
  Spinner,
  Table,
  Button,
  InputGroup,
  FormControl,
  Form,
} from "react-bootstrap";
import { JobStatusBadge } from "./JobStatusBadge";
import { FaSort, FaSortDown, FaSortUp } from "react-icons/fa";
import { Search } from "react-bootstrap-icons";
import { jobsActions, selectJobs } from "../redux/slices/jobsSlice";
import { selectJobsContainer } from "../redux/slices/JobsContainerSlice";
import { parseJobData } from "../utils/mapping";
import { getUserJobs } from "../api/maap_py";
import { openSubmitJobs, secondsToReadableString } from "../utils/utils";
import "../../style/JobsOverview.css";
import {
  MdRefresh,
} from "react-icons/md";

export const JobsOverviewContainer = ({ jupyterApp }): JSX.Element => {
  // Redux
  const dispatch = useDispatch();

  const { itemSize } = useSelector(selectJobsContainer);
  const { selectedJob, userJobInfo, jobRefreshTimestamp } =
    useSelector(selectJobs);

  const { setSelectedJob, setUserJobInfo, setJobRefreshTimestamp } =
    jobsActions;

  // Local component variables
  const [showSpinner, setShowSpinner] = useState(false);
  const [showFilters, setShowFilters] = useState(true);
  const [statusFilterOptions, setStatusFilterOptions] = useState([]);

  const data = useMemo(() => userJobInfo, [userJobInfo]);

  useEffect(() => {
    getJobInfo();
  }, []);

  useEffect(() => {
    setPageSize(itemSize);
  }, [itemSize]);

  const getJobInfo = () => {
    setShowSpinner(true);

    // List all jobs for a given user
    let response = getUserJobs();

    response
      .then((data) => {
        dispatch(setUserJobInfo(parseJobData(data["response"]["jobs"])));
      })
      .finally(() => {
        setShowSpinner(false);

        // Update refresh timestamp
        dispatch(setJobRefreshTimestamp(new Date().toUTCString()));
        // setGlobalFilter(state.globalFilter)
      });
  };

  // Set selected row
  const handleRowClick = (row) => {
    userJobInfo.map((job) => {
      if (job["payload_id"] === row.values.payload_id) {
        dispatch(
          setSelectedJob({
            rowIndex: row.index,
            jobID: row.values.payload_id,
            jobInfo: job,
          })
        );
        return;
      }
    });
  };

  const MultipleFilter = (rows, filler, filterValue) => {
    const arr = [];
    rows.forEach((val) => {
      if (filterValue.includes(val.original.status)) arr.push(val);
    });
    return arr;
  };

  function setFilteredParams(filterArr, val) {
    if (filterArr.includes(val)) {
      filterArr = filterArr.filter((n) => {
        return n !== val;
      });
    } else {
      filterArr.push(val);
    }
    return filterArr;
  }

  const SelectColumnFilter = ({
    column: { filterValue = [], setFilter, preFilteredRows, id },
  }) => {
    const options = useMemo(() => {
      const options = new Set();
      preFilteredRows.forEach((row) => {      
        options.add(row.values[id]);
      });
      setStatusFilterOptions(Array.from(options));
      return [...options.values()];
    }, [id, preFilteredRows]);

    return (
      <Fragment>
        <div className="block">
          {options.map((option: any, i) => {
            return (
              <Fragment key={i}>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    defaultChecked={true}
                    className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                    id={option}
                    name={option}
                    value={option}
                    onChange={(e) => {
                      setFilter(setFilteredParams(filterValue, e.target.value));
                    }}
                  ></input>
                  <label
                    htmlFor={option}
                    className="ml-1.5 font-medium text-gray-700"
                  >
                    {option}
                  </label>
                </div>
              </Fragment>
            );
          })}
        </div>
      </Fragment>
    );
  };

  // Text filter for a single column
  const TextColumnFilter = ({
    column: { filterValue, preFilteredRows, setFilter },
  }) => {
    const count = preFilteredRows.length;
    return (
      <div className="text-filter">
        <input
          value={filterValue || ""}
          onChange={(e) => {
            setFilter(e.target.value || undefined);
          }}
          placeholder={`Search ${count} record(s)...`}
        />
      </div>
    );
  };

  // Global text filter
  const GlobalFilter = ({
    preGlobalFilteredRows,
    globalFilter,
    setGlobalFilter,
  }: any) => {
    const [value, setValue] = React.useState(globalFilter);

    const onChange = useAsyncDebounce((value) => {
      setGlobalFilter(value || undefined);
    }, 200);

    return (
      <InputGroup className="mb-3">
        <InputGroup.Text id="basic-addon1">
          <Search />
        </InputGroup.Text>
        <FormControl
          type="search"
          key="globalSearch"
          placeholder={`Search records...`}
          aria-label="Search"
          aria-describedby="basic-addon1"
          value={value || ""}
          onChange={(e) => {
            setValue(e.target.value);
            onChange(e.target.value);
          }}
        />
      </InputGroup>
    );
  };

  // Date range filter component for a single column
  const DateRangeColumnFilter = ({
    column: { filterValue = [], preFilteredRows, setFilter, id },
  }) => {
    const [min, max] = React.useMemo(() => {
      let min = preFilteredRows.length
        ? new Date(preFilteredRows[0].values[id])
        : new Date(0);
      let max = preFilteredRows.length
        ? new Date(preFilteredRows[0].values[id])
        : new Date(0);

      preFilteredRows.forEach((row) => {
        const rowDate = new Date(row.values[id]);

        min = rowDate <= min ? rowDate : min;
        max = rowDate >= max ? rowDate : max;
      });

      return [min, max];
    }, [id, preFilteredRows]);

    return (
      <div className="date-filter">
        <input
          onChange={(e) => {
            const val = e.target.value;
            setFilter((old = []) => [val ? val : undefined, old[1]]);
          }}
          type="date"
          value={filterValue[0] || ""}
        />
        {" to "}
        <input
          onChange={(e) => {
            const val = e.target.value;
            setFilter((old = []) => [
              old[0],
              val ? val.concat("T23:59:59.999Z") : undefined,
            ]);
          }}
          type="date"
          value={filterValue[1]?.slice(0, 10) || ""}
        />
      </div>
    );
  };

  const testSort = (canSort, isSortedDesc) => {
    if (canSort) {
      if (isSortedDesc === undefined) {
        return <FaSort size={24} />;
      } else if (isSortedDesc) {
        return <FaSortDown size={24} />;
      } else {
        return <FaSortUp size={24} />;
      }
    }
  };

  const dateSort = useMemo(
    () => (rowA, rowB, columnId) => {
      // TODO: case where endtime is null but start time is not.

      if (rowA.values[columnId] === "") {
        const a = new Date(rowA.values["time_queued"]);
        const b = new Date(rowB.values[columnId]);
        return a > b ? 1 : -1;
        //return -1
      }

      if (rowB.values[columnId] === "") {
        const a = new Date(rowA.values[columnId]);
        const b = new Date(rowB.values["time_queued"]);
        return a > b ? 1 : -1;
        //return 1
      }

      const a = new Date(rowA.values[columnId]);
      const b = new Date(rowB.values[columnId]);

      return a > b ? 1 : -1;
    },
    []
  );

  // Date range filter function for a single column
  const dateBetweenFilterFn = (rows, id, filterValues) => {
    const sd = filterValues[0] ? new Date(filterValues[0]) : undefined;
    const ed = filterValues[1] ? new Date(filterValues[1]) : undefined;
    if (ed || sd) {
      return rows.filter((r) => {
        var dateAndHour = r.original[id[0]].split("T");
        var [year, month, day] = dateAndHour[0].split("-");
        var date = [month, day, year].join("/");
        var hour = dateAndHour[1];
        var formattedData = date + " " + hour;

        const cellDate = new Date(formattedData);

        if (ed && sd) {
          return cellDate >= sd && cellDate <= ed;
        } else if (sd) {
          return cellDate >= sd;
        } else {
          return cellDate <= ed;
        }
      });
    } else {
      return rows;
    }
  };

  const [hoveredRowIndex, setHoveredRowIndex] = useState(null);

  const handleRowHover = (index) => {
    setHoveredRowIndex(index);
  };

  const columns = useMemo(
    () => [
      {
        Header: "Tag",
        accessor: "tags" as const,
        disableSortBy: true,
        maxWidth: 350,
        Filter: TextColumnFilter,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>Job Type</div>,
        accessor: "job_type" as const,
        disableSortBy: true,
        maxWidth: 300,
        Filter: TextColumnFilter,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>Status</div>,
        accessor: "status" as const,
        disableSortBy: true,
        maxWidth: 300,
        Cell: ({
          cell: {
            row: {
              values: { status },
            },
          },
        }: any) => (
          <div style={{ textAlign: "center" }}>
            <JobStatusBadge status={status} />
          </div>
        ),
        Filter: SelectColumnFilter,
        filter: MultipleFilter,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>Duration</div>,
        accessor: "duration" as const,
        Cell: (row) => <div style={{ textAlign: "center" }}>{secondsToReadableString(row.value) === "" ? "-" : secondsToReadableString(row.value)}</div>,
        sortType: dateSort,
        Filter: TextColumnFilter,
        maxWidth: 300,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>Queued Time</div>,
        accessor: "time_queued" as const,
        Cell: (row) => <div style={{ textAlign: "center" }}>{row.value}</div>,
        sortType: dateSort,
        sortDescFirst: true,
        Filter: DateRangeColumnFilter,
        filter: dateBetweenFilterFn,
        maxWidth: 300,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>Start Time</div>,
        accessor: "time_start" as const,
        Cell: (row) => <div style={{ textAlign: "center" }}>{row.value}</div>,
        sortType: dateSort,
        Filter: DateRangeColumnFilter,
        filter: dateBetweenFilterFn,
        maxWidth: 300,
      },
      {
        Header: () => <div style={{ textAlign: "center" }}>End Time</div>,
        accessor: "time_end" as const,
        Cell: (row) => <div style={{ textAlign: "center" }}>{row.value}</div>,
        Filter: DateRangeColumnFilter,
        filter: dateBetweenFilterFn,
        sortType: dateSort,
        maxWidth: 300,
      },
      {
        Header: "Payload ID",
        accessor: "payload_id" as const,
        disableSortBy: true,
        maxWidth: 300,
        Filter: TextColumnFilter,
      },
    ],

    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    state,
    preGlobalFilteredRows,
    setGlobalFilter,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    visibleColumns,
    setAllFilters,
    state: { pageIndex, pageSize, sortBy },
  } = useTable(
    {
      columns,
      data: data,
      disableSortRemove: true,
      initialState: {
        pageIndex: 0,
        pageSize: itemSize,
        sortBy: [
          {
            id: "time_queued",
            desc: true,
          },
        ],
        filters: [
          {
            id: "status",
            value: statusFilterOptions
          },
        ],
      },
    },
    useFilters,
    useGlobalFilter,
    useSortBy,
    usePagination,
    useRowSelect
  );

  return (
    <div>
      <div className="overview-header">
        <div>
          <h1>My Jobs</h1>
        </div>
          <Button
            variant="primary"
            onClick={() => openSubmitJobs(jupyterApp, null)}
          >
            Submit New Job
          </Button>
      </div>
      <div className="jobs-toolbar">
        <div className="filter-toolbar">
          <Form.Check
            type="switch"
            id="toggle-filters"
            label="Show Filters"
            checked={showFilters}
            onChange={(e) => setShowFilters(e.target.checked)}
          />
          <Button
            disabled={!showFilters}
            variant="outline-primary"
            title="Reset job list filters"
            onClick={(e) => {
              setAllFilters([{ id: "status", value: statusFilterOptions }]);
              e.currentTarget.blur();
            }}
          >
            Reset Filters
          </Button>
        </div>
        <div className="refresh-toolbar">
          <Button
          variant="secondary"
            title="Refresh job list"
            onClick={(e) => {
              getJobInfo();
              e.currentTarget.blur();
            }}
          >
            <MdRefresh />
          </Button>
          {jobRefreshTimestamp ? (
            <div className="refresh-timestamp">
              List last updated:
              <br /> {jobRefreshTimestamp}
            </div>
          ) : (
            ""
          )}
        </div>
      </div>
      {/* <div className="global-filter">
                <GlobalFilter
                    preGlobalFilteredRows={preGlobalFilteredRows}
                    globalFilter={state.globalFilter}
                    setGlobalFilter={setGlobalFilter}
                />
            </div> */}
      <div className="table-container">
        <Table {...getTableProps()}>
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()} key={"Header Group"}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps()}>
                    <span
                      className="header-sort"
                      {...column.getSortByToggleProps()}
                    >
                      {column.render("Header")}
                      {testSort(column.canSort, column.isSortedDesc)}
                    </span>
                    <div>
                      {showFilters
                        ? column.canFilter
                          ? column.render("Filter")
                          : null
                        : null}
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          {showSpinner ? (
            <tbody>
              <tr key={"loading-jobs"}>
                <td colSpan={columns.length} style={{ textAlign: "center" }}>
                  <Spinner animation="border" variant="primary" />
                </td>
              </tr>
            </tbody>
          ) : (
            <tbody {...getTableBodyProps()}>
              {page.map((row) => {
                prepareRow(row);
                return (
                  <tr
                    key={row.index}
                    className={
                      selectedJob && selectedJob.rowIndex === row.index
                        ? "selected-row position-relative"
                        : "position-relative"
                    }
                    onClick={() => handleRowClick(row)}
                    onMouseEnter={() => handleRowHover(row.index)}
                    onMouseLeave={() => handleRowHover(null)}
                  >
                    {row.cells.map((cell) => {
                      return (
                        <td
                          className="cell-overflow"
                          {...cell.getCellProps({
                            style: {
                              maxWidth: cell.column.maxWidth,
                            },
                          })}
                        >
                          {cell.render("Cell")}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          )}
        </Table>
      </div>
      <div className="pagination">
        <Pagination>
          <Pagination.First
            onClick={() => gotoPage(0)}
            disabled={!canPreviousPage}
          />
          <Pagination.Prev
            onClick={() => previousPage()}
            disabled={!canPreviousPage}
          />
          <Pagination.Next onClick={() => nextPage()} disabled={!canNextPage} />
          <Pagination.Last
            onClick={() => gotoPage(pageCount - 1)}
            disabled={!canNextPage}
          />
        </Pagination>
        <span>
          Page {pageOptions.length === 0 ? 0 : pageIndex + 1} of{" "}
          {pageOptions.length}
        </span>
      </div>
    </div>
  );
};
