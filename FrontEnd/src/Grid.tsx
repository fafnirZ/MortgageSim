import styled from "styled-components";

interface GridProps {
    columns: number;
    rows: number;
}

const Grid = styled.div<GridProps>`
    display: grid;
    grid-template-columns: repeat(${(props) => props.columns}, 1fr));
    grid-template-rows: repeat(${(props) => props.rows}}, 1fr);
    gap: 1vw;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
`;

export default Grid;