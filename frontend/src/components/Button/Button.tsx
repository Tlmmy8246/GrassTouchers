import { ButtonProps } from "./Button.types";
import React from "react";

const Button: React.FC<ButtonProps> = ({ className, ...rest }) => {
	return (
		<button className={[className, "cursor-pointer p-2 w-fit bg-gray-400/50 border-black border-3 hover:bg-gray-400/75"].join(" ")} {...rest}>{rest.children}</button>
	)
}

export default Button
