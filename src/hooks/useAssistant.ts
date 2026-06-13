import { useEffect, useState } from "react";

export function useAssistant() {
  const [works, worksSet] = useState("wait");

  useEffect(() => {
    setTimeout(() => {
      worksSet("hearing");
      setTimeout(() => {
        worksSet("processing");
        setTimeout(() => {
          worksSet("speaking");
          setTimeout(() => {
            worksSet("wait");
          }, 2000);
        }, 3000);
      }, 3000);
    }, 3000);
  }, []);
  return { works };
}
