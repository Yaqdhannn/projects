function ListGroup() {
  let items = ["New York", "San Fran", "Tokyo", "London", "Paris"];
  items = [];

  const getMessage = () => {
    return items.length === 0 ? <p>No item</p> : null;
  }

  return (
    <>
      <h1>List</h1>
      {getMessage()}
      {/* another way to write this: */}
      {/* if first condition is true then code after && happens, if not then nothing happens */}
      {/* {items.length === 0 && <p>No item</p>}  */}
      <ul className="list-group">
        {items.map((item) => (
          <li key={item} className="list-group-item list-group-item-action">
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
