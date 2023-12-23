import { MouseEvent, useState } from "react";

interface Props {
  items: string[];
  heading: string;
  onSelectItem: (item: string) => void;
}

function ListGroup({ items, heading, onSelectItem }: Props) {
  // Hook function
  const [selectedIndex, setSelectedIndex] = useState(-1);
  // arr[0] is variable (like selectedIndex)
  // arr[1] is updater function

  const getMessage = () => {
    return items.length === 0 ? <p>No item</p> : null;
  };

  // Handler function
  // const handleClick = (event: MouseEvent) => console.log(event.type);

  return (
    <>
      <h1>{heading}</h1>
      {getMessage()}
      {/* another way to write this: */}
      {/* if first condition is true then code after && happens, if not then nothing happens */}
      {/* {items.length === 0 && <p>No item</p>}  */}
      <ul className={"list-group"}>
        {items.map((item, index) => (
          <li
            key={item}
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            onClick={() => {
              setSelectedIndex(index);
              onSelectItem(item);
            }}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
