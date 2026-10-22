interface ActionButtonProps {label:string;variant?:"solid"|"outline";disabled?:boolean;onClick?:()=>void}
interface FlavorTagProps {label:string}
interface ProductCardProps {name:string;series?:string;flavor?:string;description?:string;price?:string;image?:string;action?:string;onClick?:()=>void}
declare const STILL:{ActionButton(p:ActionButtonProps):HTMLButtonElement;FlavorTag(p:FlavorTagProps):HTMLSpanElement;ProductCard(p:ProductCardProps):HTMLElement};