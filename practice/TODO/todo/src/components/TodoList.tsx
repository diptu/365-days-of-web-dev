import React from 'react'
import Todo from './Todo'
type listProps = {
  id : number,
  title : string,
  description : string
}



const TodoList = (props: listProps) => {
  
  return (
    <div>
      {
        props.todos.map((todo) => (
          <Todo todo={todo} key={todo.id}/>
        ))
      }
    </div>
  )
}

export default TodoList
