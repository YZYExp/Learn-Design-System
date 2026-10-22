declare namespace FieldNotes {
function Masthead(props?: {name?: string; english?: string; issue?: string}): HTMLElement;
function EditorialCaption(props?: {number?: string; text?: string}): HTMLElement;
function EventBadge(props?: {date?: string; label?: string}): HTMLElement;
function Cover(): HTMLElement;
}
