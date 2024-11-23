import React from 'react'

type TodoProps = {

  id: number,
  title: string,
  description: string
}
const Todo = (props:TodoProps) => {
  return (
    <div>
      <h3>Title : {props.todo.title}</h3>
      <p>Description : {props.todo.description}</p>
    </div>
  )
}

export default Todo
