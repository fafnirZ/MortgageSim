import styles from "./Button.module.css";


export function Button({ 
    colour: string, 
    content: string,
    onClick: callable,

}) {
    return (
        <div 
            className={styles.BaseStyle}
            style={{
                "backgroundColor": color
            }}
        >
            {content}
        </div>
    )
}