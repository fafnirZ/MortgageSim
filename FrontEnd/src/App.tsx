import styled from "styled-components"
import Box from "./Box"
import Grid from "./Grid"

const PageWrapper = styled.div`
  height: 100vh;
  display: flex;
`
const Content = styled.div`
  width: 85%;
  height: 100%;
`

const Container = styled.div`
  width: 100%;
  height: 90%;
  max-width: 100vw;
  overflow: hidden;
  background-color: #f0f0f0;
`
const Header = styled.div`
  height: 10%;
  text-align: center;
  background-color: grey;
`

const SideBar = styled.div`
  height 100%;
  width: 15%;
  background-color: blue;
`

function App() {

  return (
    <PageWrapper>
      <SideBar>Side Bar </SideBar>
      <Content>
        <Header>Header</Header>
        <Container>
          <Grid columns={4} rows={7}>
              <Box columns={1} rows={1} startColumn={1} startRow={1}>Box 1 (1x1)</Box>
              <Box columns={1} rows={1} startColumn={2} startRow={1}>Box 2 (1x1)</Box>
              <Box columns={1} rows={1} startColumn={3} startRow={1}>Box 3 (1x1)</Box>
              <Box columns={1} rows={1} startColumn={4} startRow={1}>Box 4 (1x1)</Box>
              <Box columns={2} rows={4} startColumn={1} startRow={2}>Box 5 (2x4)</Box>
              <Box columns={1} rows={3} startColumn={3} startRow={2}>Box 6 (1x3)</Box>
              <Box columns={1} rows={4} startColumn={4} startRow={2}>Box 7 (1x4)</Box>
              <Box columns={1} rows={1} startColumn={3} startRow={5}>Box 8 (1x1)</Box>
              <Box columns={3} rows={2} startColumn={1} startRow={6}>Box 9 (3x2)</Box>
              <Box columns={1} rows={1} startColumn={4} startRow={6}>Box 10 (1x1)</Box>
              <Box columns={1} rows={1} startColumn={4} startRow={7}>Box 11 (1x1)</Box>
          </Grid>
        </Container>
      </Content>
    </PageWrapper>
  )
}

export default App
