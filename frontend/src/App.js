import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hello guys!
        </p>
        <a
          className="App-link"
          href="https://github.com/users/dmtnikolaev/projects/1/views/1"
          target="_blank"
          rel="noopener noreferrer"
        >
          Taskboard
        </a>
        <a
          className="App-link"
          href="https://github.com/users/dmtnikolaev/projects/2"
          target="_blank"
          rel="noopener noreferrer"
        >
          Roadmap
        </a>
      </header>
    </div>
  );
}

export default App;
