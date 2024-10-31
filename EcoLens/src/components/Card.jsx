
function Card(props) { 

const {title, description} = props;
  return (
    
    <article className="card">
        <header>
          <h2 className="heading">{title}</h2>
        </header>
        <img src="todo.png" alt="To DO List" className="thumbnail" />
        <div className="content">
          <p> {props.description} </p>
        </div>
    </article>

  )
 }
 export default Card