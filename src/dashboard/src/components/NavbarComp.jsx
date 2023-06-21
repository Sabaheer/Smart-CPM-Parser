import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";

function NavbarComp() {
  return (
    <Navbar expand="lg" variant="dark" bg="dark" className="mb-4 shadow">
      <Container>
        <Navbar.Brand href="#">Etihad Smart CPM parser</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default NavbarComp;
