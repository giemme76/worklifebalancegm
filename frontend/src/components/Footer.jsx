export default function Footer() {
  return (
    <div className="shrink-0 px-5 py-2.5 border-t border-line bg-surface text-center">
      <div className="text-[11px] text-muted">
        Realizzato da{" "}
        <a
          href="https://giemme76.com/"
          target="_blank"
          rel="noreferrer"
          className="font-bold text-office"
        >
          Giemme76
        </a>{" "}
        (
        <a
          href="https://www.linkedin.com/company/giemme76/"
          target="_blank"
          rel="noreferrer"
          className="font-bold text-office"
        >
          LinkedIn
        </a>
        )
      </div>
    </div>
  );
}
