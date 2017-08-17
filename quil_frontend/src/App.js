import React, { Component } from 'react';
import $ from 'jquery';
import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {
  AppBar,
  TextField,
  CircularProgress,
  RaisedButton,
  Divider,
} from 'material-ui';
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';
import './App.css';

export default function App({ mode = 'production' }) {
  // material-ui shim so touch events work properly
  injectTapEventPlugin();

  return (
    <MuiThemeProvider>
      <div className="App">
        <AppHeader />
        <AppBody mode={mode} />
      </div>
    </MuiThemeProvider>
  );
}

function AppHeader() {
  return <AppBar title="Quil Evaluator" />;
}

export class AppBody extends Component {
  constructor(props) {
    super(props);
    this.onClickEval = this.onClickEval.bind(this);
    this.handleQuilChange = this.handleQuilChange.bind(this);
    this.state = {
      evalInProgress: false,
      quilString: '',
      memResult: '',
      wfResult: '',
      url: props.mode === 'development'
        ? 'http://localhost:5000/measure'
        : 'measure',
    };
  }
  handleQuilChange = event => {
    this.setState({ quilString: event.target.value });
  };
  onClickEval() {
    this.setState({ evalInProgress: true, memResult: '', wfResult: '' });
    const data = { quil_string: this.state.quilString };

    $.post(this.state.url, data)
      .done((res, status) => {
        if (status === 'success') {
          this.setState({
            memResult: res.mem,
            wfResult: res.wf,
            evalInProgress: false,
          });
        }
      })
      .fail(() => {
        const errorMsg = 'Error received from server';
        this.setState({
          memResult: errorMsg,
          wfResult: errorMsg,
          evalInProgress: false,
        });
      });
  }
  render() {
    return (
      <div id="app-body" className="flex-container">
        <div className="flex-item">
          <TextField
            hintText="Enter your Quil commands here"
            multiLine={true}
            rows={2}
            rowsMax={10}
            value={this.state.quilString}
            onChange={this.handleQuilChange}
            style={{ display: 'block' }}
          />
          <RaisedButton
            label="Evaluate"
            primary={true}
            onClick={this.onClickEval}
            style={{ display: 'block', maxWidth: '150px' }}
          />
        </div>
        <br />
        <br />
        <Divider />
        <br />
        <br />
        {this.state.evalInProgress
          ? <div className="spinner flex-item"><CircularProgress /></div>
          : <OutputField
              wfResult={this.state.wfResult}
              memResult={this.state.memResult}
            />}
      </div>
    );
  }
}

function OutputField({ wfResult, memResult }) {
  return (
    <Table selectable={false}>
      <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
        <TableRow>
          <TableHeaderColumn>Result Type</TableHeaderColumn>
          <TableHeaderColumn>Output</TableHeaderColumn>
        </TableRow>
      </TableHeader>
      <TableBody displayRowCheckbox={false}>
        <TableRow>
          <TableRowColumn>Wave Function</TableRowColumn>
          <TableRowColumn>{wfResult}</TableRowColumn>
        </TableRow>
        <TableRow>
          <TableRowColumn>Classical Measurement</TableRowColumn>
          <TableRowColumn>{memResult}</TableRowColumn>
        </TableRow>
      </TableBody>
    </Table>
  );
}
