import { useId, type InputHTMLAttributes } from 'react';
import styles from './TextField.module.css';

type TextFieldProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
};

// SRP: input de texto controlado desde el padre, con etiqueta accesible.
export function TextField({ label, id, className, ...rest }: TextFieldProps) {
  const generatedId = useId();
  const fieldId = id ?? generatedId;
  return (
    <div className={styles.field}>
      <label htmlFor={fieldId} className={styles.label}>
        {label}
      </label>
      <input
        id={fieldId}
        className={[styles.input, className].filter(Boolean).join(' ')}
        {...rest}
      />
    </div>
  );
}
