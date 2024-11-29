import React from 'react'

type TodoProps = {

  id: number,
  title: string,
  description: string
}
const Todo = (props:TodoProps) => {
  const {  title , description} = props.todo
  return (
    <article>
        <div>
      <h3>Title : {title}</h3>
      <p>Description : {description}</p>
    </div>
    <button>
    <i className="fa-solid fa-trash"></i>
    </button>
    </article>
    
  )
}

export default Todo
