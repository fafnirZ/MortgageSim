import styled from "styled-components"

interface BoxProps {
    columns: number;
    rows: number;
    startColumn: number;
    startRow: number;
}

const Box = styled.div<BoxProps>`
    border: 2px solid black;

    grid-column: ${(props) => props.startColumn} / span ${(props) => props.columns};
    grid-row: ${(props) => props.startRow} / span ${(props) => props.rows};
`;

export default Box;