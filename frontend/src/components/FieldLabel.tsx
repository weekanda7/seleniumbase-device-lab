import { ReactNode } from "react";

/** Form field title. testid spec "field trio": {name}-field (label) / {name}-input / {name} (read-only value). */
export default function FieldLabel({ name, children }: { name: string; children: ReactNode }) {
  return <span data-testid={`${name}-field`}>{children}</span>;
}
