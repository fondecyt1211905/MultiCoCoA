import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Nav, Navbar } from 'react-bootstrap';
import {Route, Routes, Link} from 'react-router-dom';

// import views
import Home from "./components/views/home.component";
import NotFound from "./components/views/notFound.component";
import Activities from "./components/activities/activities.component";
import Files from "./components/files/files.component";
import CreateActivities from "./components/activities/createActivities.component";
import Analysis from "./components/analysis/analysis.component";
import Indicator from "./components/indicator/indicators.component";

function App() {
  return (
    <div className="App">
      <header className="header">
        <Navbar bg="light" expand="lg">
          <Container>
            <Navbar.Brand href="/home">
              <img
                alt=""
                src={logo}
                width="30"
                height="30"
                className="d-inline-block align-top"
              />{' '}
              Virtual Device
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
              <Nav className="me-auto">
                <Link to={"/home"} className="nav-link">
                  Home
                </Link>
                <Link to={"/activities"} className="nav-link">
                  Activities
                </Link>
                <Link to={"/analysis"} className="nav-link">
                  Analysis
                </Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </header>
      <section>
        <Container>
          <Routes>
            <Route exact path="/" element={<Home />}/>
            <Route exact path="/home" element={<Home />}/>
            <Route exact path="/activities" element={<Activities />}/>
            <Route exact path="/activity/files/:name" element={<Files />}/>
            <Route exact path="/create-activity" element={<CreateActivities />}/>
            <Route exact path="/analysis" element={<Analysis />}/>
            <Route exact path="/indicator/:id_analysis" element={<Indicator />}/>
            <Route path='*' element={<NotFound />}/>
          </Routes>
        </Container>
      </section>
      <footer className='mt-auto py-3 bg-light'>
      <Navbar bg="light">
        <Container>
          <Navbar.Brand href="#home">© uv.cl</Navbar.Brand>
        </Container>
      </Navbar>
      </footer>
    </div>
  );
}

export default App;
