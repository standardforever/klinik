import styled, { css } from "styled-components";

export const Icon = styled.div`
  ${(props) =>
    props.service &&
    css`
      border-radius: 5px;
      background-color: #0765fe;
      text-align: center;
      color: #fff;
      display: inline-block;
      padding: 5px;
      font-size: 1.3rem;
    `}
  ${(props) =>
    props.ft &&
    css`
      font-size: 1.5rem;
    `}
    ${(props) =>
    props.sb &&
    css`
      font-size: 2.1rem;
    `}
    ${(props) =>
    props.header &&
    css`
      font-size: 1.5rem;
      box-shadow: 4px 4px 8px 0 rgba(0, 0, 0, 0.25),
        -2px -2px 6px 0 rgba(255, 255, 255, 0.3);
      text-align: center;
      border-radius: 100%;
      padding: 4px 7px;
    `}
    ${(props) =>
    props.detail &&
    css`
      color: #0765fe;
      display: flex;
      align-items: center;
    `}
    ${(props) =>
    props.add &&
    css`
      position: fixed;
      right: 75px;
      bottom: 75px;
      color: #0765fe;
      font-size: 4rem;
    `}
`;