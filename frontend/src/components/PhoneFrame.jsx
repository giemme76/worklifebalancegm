/**
 * Contenitore che centra l'app in una card in stile "telefono" su schermi larghi,
 * riprendendo l'anteprima 393x852 del design; su mobile occupa tutto lo schermo.
 */
export default function PhoneFrame({ children }) {
  return (
    <div className="min-h-screen bg-[#efece6] flex items-center justify-center p-0 sm:p-10">
      <div
        className="w-full sm:w-[393px] h-screen sm:h-[844px] sm:max-h-[90vh] bg-bg
                   sm:rounded-[40px] sm:shadow-2xl sm:border-8 sm:border-ink overflow-hidden
                   flex flex-col relative"
      >
        {children}
      </div>
    </div>
  );
}
