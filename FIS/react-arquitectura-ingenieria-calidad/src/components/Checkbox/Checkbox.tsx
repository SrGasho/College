import { useId, type InputHTMLAttributes } from 'react';
import styles from './Checkbox.module.css';

type CheckboxProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> & {
  label: string;
};

// SRP: checkbox con etiqueta accesible, controlado desde el padre.
export function Checkbox({ label, id, className, ...rest }: CheckboxProps) {
  const generatedId = useId();
  const fieldId = id ?? generatedId;
  return (
    <span className={styles.wrapper}>
      <input id={fieldId} type="checkbox" className={className} {...rest} />
      <label htmlFor={fieldId} className={styles.label}>
        {label}
      </label>
    </span>
  );
}
