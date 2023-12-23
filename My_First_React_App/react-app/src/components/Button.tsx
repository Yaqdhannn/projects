import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  onClick: () => void;
}

function Button({ children, onClick }: Props) {
  return (
    <button type="button" className="btn btn-primary" onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
