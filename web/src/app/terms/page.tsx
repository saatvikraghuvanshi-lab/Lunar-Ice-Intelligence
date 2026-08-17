import Link from "next/link";

import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const sections = [
  {
    title: "Prototype purpose",
    copy: "Lunar Ice Intelligence is a hackathon decision-support prototype for screening candidate lunar south-pole targets using public and downloaded mission data products. It is intended for planning, education, and demonstration.",
  },
  {
    title: "No confirmed ice claim",
    copy: "Outputs must be interpreted as candidate evidence only. The platform does not confirm water ice, resource availability, landing safety, or rover traversability.",
  },
  {
    title: "Scientific validation limits",
    copy: "LOLA validation is coarse regional validation. Cold-trap and illumination outputs require ephemeris-grade validation. OHRC hazard context requires footprint registration before exact overlap claims.",
  },
  {
    title: "User responsibilities",
    copy: "Users are responsible for reviewing source provenance, assumptions, and confidence notes before using any output in a report, presentation, or downstream analysis.",
  },
  {
    title: "Data and account use",
    copy: "Account information is used to authenticate users and record terms acceptance. Do not upload sensitive credentials, private mission data, or personal information beyond what is required for access.",
  },
  {
    title: "Availability",
    copy: "The service may change, fail, or be unavailable during active development. No warranty is provided for scientific, operational, legal, or mission-critical use.",
  },
];

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#0f0e0e] px-6 py-10 text-white">
      <div className="mx-auto grid max-w-4xl gap-6">
        <div className="flex items-center justify-between gap-4">
          <Link href="/" className="text-sm font-medium text-[#ff8a98]">
            Lunar Ice Intelligence
          </Link>
          <Link className={buttonVariants({ variant: "outline", size: "sm" })} href="/signup">
            Back to signup
          </Link>
        </div>
        <Card>
          <CardHeader>
            <p className="text-sm uppercase tracking-normal text-[#ff8a98]">
              Terms of Use
            </p>
            <CardTitle className="text-3xl">Clear rules for a scientific prototype</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-5">
            <p className="leading-7 text-white/70">
              Last updated: June 19, 2026. These terms are written for the
              hackathon prototype and should be reviewed by counsel before any
              public or production launch.
            </p>
            <div className="grid gap-4">
              {sections.map((section) => (
                <section key={section.title} className="rounded-md border border-white/15 bg-white/[0.04] p-4">
                  <h2 className="font-semibold text-white">{section.title}</h2>
                  <p className="mt-2 leading-7 text-white/70">{section.copy}</p>
                </section>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
