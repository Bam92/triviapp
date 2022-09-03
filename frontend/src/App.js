import React, { Component, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
// import { data } from 'jquery';

const Categories = () => {
  useEffect(() => {
    fetch(`http://localhost:4000/`)
    .then(response => response.json())
    .then(actualData => console.log(actualData))
  }, [])

  return (
    <h1>Hello</h1>
  )
}

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header path />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route path='/test' component={Categories} />
            <Route path='/play' component={QuizView} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
